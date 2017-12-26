# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import re
import urlparse
import redis

from pyquery import PyQuery as PQ

from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy.http import Request

from bookspider.items import BookinfoItem, BookpageItem

BASE_URL = "https://www.xs.la"
BOOK_INFO_URL_RE = re.compile(r"https:\/\/www\.xs\.la\/(?P<book_id>\d+_\d+)\/$")
BOOK_PAGE_URL_RE = re.compile(r"https:\/\/www\.xs\.la\/(?P<book_id>\d+_\d+)\/(?P<page_id>\d+)\.html")
PASS_URL = ['login.php', 'bookcase.php', 'Login.php', 'index.php', 'bookcase.php']
RC = redis.Redis()


class BiqugeSpider(Spider):
    name = "biquge"
    allowed_domains = ["www.xs.la"]

    def __init__(self, starturl=None, frombookid=None, frombookidrange=None, fromexistbooks=False, onlybookinfo=False,
                 *args, **kwargs):
        super(BiqugeSpider, self).__init__(*args, **kwargs)
        self.onlybookinfo = bool(onlybookinfo)
        self.start_urls = [
            "https://www.xs.la",
        ]
        if starturl:
            self.start_urls = starturl.split(" ")
        if frombookid:
            self.start_urls = ["https://www.xs.la/{0}/".format(bid) for bid in frombookid.split(" ")]
        if fromexistbooks:
            from bookspider.items import Book
            book_number_list = Book.objects.filter(site='xs.la').values_list('book_number', flat=True)
            self.start_urls = ["https://www.xs.la/{0}/".format(bid) for bid in book_number_list]
        print "-" * 20
        print "Start from:\n", '\n'.join(self.start_urls)
        print "-" * 20, "\n"

    def is_pass_url(self, url):
        for i in PASS_URL:
            if i in url:
                return True
        return False
    
    def get_no_query_url(self, url):
        url_p = urlparse.urlparse(url)
        return urlparse.urljoin(url_p.geturl(), url_p.path)

    def parse_book_info(self, response):
        """获取书籍信息"""
        url = self.get_no_query_url(response.url)
        sel = Selector(response)
        jQ = PQ(response.body_as_unicode())
        book = BookinfoItem()
        book['site'] = "xs.la"
        book['book_number'] = BOOK_INFO_URL_RE.match(url).groupdict()['book_id']
        book['origin_url'] = url
        book['title'] = jQ("#info h1").text()
        book['author'] = jQ('meta[property="og:novel:author"]').attr('content')
        book['category'] = jQ('meta[property="og:novel:category"]').attr('content')
        book['info'] = jQ('#intro').text().replace(" ", "\n")
        book['image_urls'] = [jQ('meta[property="og:image"]').attr('content')]
        return book
    
    def parse_page(self, response):
        """获取章节信息"""
        url = self.get_no_query_url(response.url)
        sel = Selector(response)
        jQ = PQ(response.body_as_unicode())
        page = BookpageItem()
        page['site'] = "xs.la"
        page['origin_url'] = url
        next_href = self.get_next_page_url(response)
        prev_href = self.get_prev_page_url(response)
        if RC.get(page['origin_url']):
            if next_href is not None and not RC.get(next_href):
                return Request(next_href, callback=self.parse)
            if prev_href is not None and not RC.get(prev_href):
                return Request(prev_href, callback=self.parse)
        else:
            page['title'] = jQ('h1').text()
            if not page['title'].strip():
                raise TypeError('Page No Title!')
            page['content'] = jQ("#content").text().replace(" ", "\n")
            page['book_number'] = BOOK_PAGE_URL_RE.match(url).groupdict()['book_id']
            page['page_number'] = BOOK_PAGE_URL_RE.match(url).groupdict()['page_id']
            if BOOK_PAGE_URL_RE.match(prev_href):
                page['prev_number'] = BOOK_PAGE_URL_RE.match(prev_href).groupdict()['page_id']
            else:
                page['prev_number'] = None
            if BOOK_PAGE_URL_RE.match(next_href):
                page['next_number'] = BOOK_PAGE_URL_RE.match(next_href).groupdict()['page_id']
            else:
                page['next_number'] = None
            return page

    def parse(self, response):
        url = self.get_no_query_url(response.url)
        sel = Selector(response)
        jQ = PQ(response.body_as_unicode())
        # 跳过cdn未命中
        if 'cache.51cdn.com' in response.body_as_unicode():
            # print response.body_as_unicode()
            # print response.headers
            href = jQ('head script').text().split("'")[1]
            print "Retry: " + href
            yield Request(href, callback=self.parse)
        # 书页
        elif BOOK_INFO_URL_RE.match(url):
            # 书籍信息
            yield self.parse_book_info(response)
            # 书目
            hrefs = sel.xpath('//*[@id="list"]/dl/dd/a/@href').extract()
            for href in hrefs:
                rel_url = urlparse.urljoin(url, href)
                # 去重
                if RC.get(rel_url):
                    continue
                yield Request(rel_url, callback=self.parse)
        # 章节
        elif BOOK_PAGE_URL_RE.match(url) and not self.onlybookinfo:
            yield self.parse_page(response)
        # 继续爬行
        elif not self.onlybookinfo:
            for href in sel.xpath("//a/@href").extract():
                if self.is_pass_url(href):
                    continue
                if not href.startswith('javascript:') and href != '/' and not href.startswith("#"):
                    href = urlparse.urljoin(url, href)
                    # 去掉重复章节
                    if RC.get(href):
                        continue
                    # 去掉重复书页
                    if BOOK_INFO_URL_RE.match(href):
                        book_number = BOOK_INFO_URL_RE.match(href).groupdict()['book_id']
                        if RC.hget('books', str(book_number)):
                            continue
                    yield Request(href, callback=self.parse)

    def get_next_page_url(self, response):
        jQ = PQ(response.body_as_unicode())
        return urlparse.urljoin(response.url, jQ('#pager_next').attr('href'))

    def get_prev_page_url(self, response):
        jQ = PQ(response.body_as_unicode())
        return urlparse.urljoin(response.url, jQ('#pager_prev').attr('href'))
