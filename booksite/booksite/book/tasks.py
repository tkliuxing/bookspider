# -*- coding: utf-8 -*-
# import subprocess
import re
import difflib
import requests
import urlparse
from pyquery import PyQuery as PQ

from celery import shared_task

from booksite.book.models import BookPage, Book


class RequestError(Exception):
    pass

# def update_book(book_number):
#     subprocess.Popen("/root/Envs/book/bin/scrapy \
#       parse http://www.86696.cc/book/%d.html \
#       --depth 4 --pipelines --noitems --nolinks -L ERROR" % book_number)


def get_book_index(book_title):
    """从 '小说库' 获得指定书名的书籍目录."""
    headers = {
        'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36"
    }
    data = {"searchkey": book_title.encode("gbk"), "searchtype": "articlename"}
    url = "http://www.xiaoshuoku.com/search"
    search_book_req = requests.post(url, data=data, headers=headers)
    search_book_req.encoding = 'gbk'
    if not search_book_req.history:
        print search_book_req.text
        raise RequestError("Book not found! status_code: %s" % search_book_req.status_code)
    jq = PQ(search_book_req.text)
    book_index_url = jq("a.fl.btn")[0].attrib['href']
    book_index_req = requests.get(book_index_url, headers=headers)
    book_index_req.encoding = 'gbk'
    return book_index_req.text[:], book_index_req.url


def cmppmax(sa, sb):
    """获取字符串最大匹配长度,用来对比查找章节标题"""
    s = difflib.SequenceMatcher(None, sa, sb)
    max_len = 0
    for tag, i1, i2, j1, j2 in s.get_opcodes():
        if tag == 'equal':
            max_len = i2 - i1 if i2 - i1 > max_len else max_len
    return max_len


def get_bookpage_match_url(book_index, page_title):
    """从章节目录获得匹配的章节url"""
    if isinstance(book_index, PQ):
        jq = book_index
    elif isinstance(book_index, (unicode, str)):
        jq = PQ(book_index)
    else:
        raise TypeError
    match_a = None
    match_a_max_len = 0
    for i, elem in enumerate(jq("dd>a")):
        match_len = cmppmax(page_title, elem.text)
        if match_len > match_a_max_len:
            match_a_max_len = match_len
            match_a = elem
    return match_a.attrib["href"]


def get_page_content(page_url):
    """获取章节内容"""
    headers = {
        'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36"
    }
    page_req = requests.get(page_url, headers=headers)
    page_req.encoding = 'gbk'
    jq = PQ(page_req.text)
    content = jq("#text_area").text().replace(" ", "\n")
    rp = re.compile(r".*(\[.*\]).*")
    for i in rp.findall(content):
        content = content.replace(i, '')
    return content


@shared_task
def update_page(page_id, book_title, page_title):
    """更新指定章节的内容"""
    book_index_html, book_index_url = get_book_index(book_title)
    page_url = get_bookpage_match_url(book_index_html, page_title)
    page_url = urlparse.urljoin(book_index_url, page_url)
    content = get_page_content(page_url)
    page = BookPage.objects.get(pk=page_id)
    page.content = content
    page.save()
    return content


@shared_task
def update_book_pic_page(book_number, page_min_length):
    """更新指定书籍的图片章节,按照page_min_length判断章节长度,小于此长度则更新."""
    book = Book.objects.get(book_number=book_number)
    book_index_html, book_index_url = get_book_index(book.title)
    book_index = PQ(book_index_html)
    pages = BookPage.objects.filter(book_number=book_number)
    for page in pages:
        if len(page.content) < page_min_length:
            page_url = get_bookpage_match_url(book_index, page.title)
            page_url = urlparse.urljoin(book_index_url, page_url)
            content = get_page_content(page_url)
            page.content = content
            page.save()
    return list(pages.values_list("pk", flat=True))


