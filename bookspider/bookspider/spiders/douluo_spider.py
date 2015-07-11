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

BASE_URL = "http://www.86696.cc"
BOOK_INFO_URL_RE = re.compile(r"http:\/\/www\.86696\.cc\/book/(?P<book_id>\d+)\.html")
BOOK_INDEX_URL_RE = re.compile(r"http:\/\/www\.86696\.cc\/html\/\d+\/(?P<book_id>\d+)\/$")
BOOK_PAGE_URL_RE = re.compile(r"http:\/\/www\.86696\.cc\/html\/\d+\/(?P<book_id>\d+)\/(?P<page_id>\d+)\.html")
PASS_URL = ['login.php', 'newmessage.php', 'charset=', 'index.php']
RC = redis.Redis()


class DouluoSpider(Spider):
    name = "douluo"
    allowed_domains = ["www.86696.cc"]

    def __init__(self, starturl=None, frombookid=None, frombookidrange=None, *args, **kwargs):
        super(DouluoSpider, self).__init__(*args, **kwargs)
        self.start_urls = [
            "http://www.86696.cc/booktoppostdate/0/1.html",
            "http://www.86696.cc/booktoplastupdate/0/1.html",
        ]
        if starturl:
            self.start_urls = starturl.split(" ")
        if frombookid:
            self.start_urls = ["http://www.86696.cc/book/%s.html" % bid for bid in frombookid.split(" ")]
        if frombookidrange:
            try:
                fr, to = frombookidrange.split()
                fr, to = int(fr), int(to)
            except:
                raise AttributeError("frombookidrange format error! Should like this: '10 20'.")
            self.start_urls = ["http://www.86696.cc/book/%s.html" % bid for bid in range(fr, to)]
        print "-"*20
        print "Start from:\n", '\n'.join(self.start_urls)
        print "-"*20, "\n"

    def is_pass_url(self, url):
        for i in PASS_URL:
            if i in url:
                return True
        return False

    def parse(self, response):
        url = response.url
        sel = Selector(response)
        jQ = PQ(response.body_as_unicode())
        # 书页
        if BOOK_INFO_URL_RE.match(url):
            book = BookinfoItem()
            book['book_number'] = BOOK_INFO_URL_RE.match(url).groupdict()['book_id']
            # 去重
            if RC.hget('books', str(book['book_number'])):
                # 书籍重复则进入目录抓取章节
                hrefs = sel.css(".button2.white").xpath('a[1]/@href').extract()
                for href in hrefs:
                    rel_url = urlparse.urljoin(url, href)
                    yield Request(rel_url, callback=self.parse)
            else:
                # 否则生成书籍信息
                book['origin_url'] = url
                book['title'] = jQ("h1").text()
                book['author'] = jQ("h2").eq(0).text().replace(u"作者：", "")
                book['category'] = jQ("h2").eq(2).text().replace(u"所属：", "")
                book['info'] = jQ(".msgarea>p").text().replace(" ", "\n")
                yield book
                hrefs = sel.css(".button2.white").xpath('a[1]/@href').extract()
                for href in hrefs:
                    rel_url = urlparse.urljoin(url, href)
                    yield Request(rel_url, callback=self.parse)
        # 书目
        elif BOOK_INDEX_URL_RE.match(url):
            hrefs = sel.xpath("//dl/dd/a/@href").extract()
            for href in hrefs:
                rel_url = urlparse.urljoin(url, href)
                # 去重
                if RC.get(rel_url):
                    continue
                yield Request(rel_url, callback=self.parse)
        # 章节
        elif BOOK_PAGE_URL_RE.match(url):
            page = BookpageItem()
            page['origin_url'] = url
            next_href = self.get_next_page_url(response)
            prev_href = self.get_prev_page_url(response)
            # 去重并尝试下一页
            if RC.get(page['origin_url']):
                next_rel_href = urlparse.urljoin(url, next_href)
                prev_rel_href = urlparse.urljoin(url, prev_href)
                if not RC.get(next_rel_href):
                    yield Request(next_rel_href, callback=self.parse)
                if not RC.get(prev_rel_href):
                    yield Request(prev_rel_href, callback=self.parse)
            else:
                page['title'] = sel.xpath('//h1/text()').extract()[0]
                page['content'] = jQ('#BookText').text().replace(" ", "\n")
                page['book_number'] = BOOK_PAGE_URL_RE.match(url).groupdict()['book_id']
                page['page_number'] = BOOK_PAGE_URL_RE.match(url).groupdict()['page_id']
                page_number_re = re.compile(r'(?P<number>\d+).+')
                if page_number_re.match(prev_href):
                    page['prev_number'] = page_number_re.match(prev_href).groupdict()['number']
                else:
                    page['prev_number'] = None
                if page_number_re.match(next_href):
                    page['next_number'] = page_number_re.match(next_href).groupdict()['number']
                else:
                    page['next_number'] = None
                yield page
        # 继续爬行
        else:
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

    def get_npage_url(self, response, page_a=2):
        sel = Selector(response)
        next_href = sel.xpath('//div[@class="fanye"]/a[%d]/@href' % (page_a+1)).extract()
        if not next_href:
            rrr = re.compile(r'.*返回目录.*')
            fanye_line = rrr.findall(response.body_as_unicode())
            if not fanye_line:
                return 'index.html'
            else:
                jQ = PQ(fanye_line[0])
                return jQ('a').eq(page_a).attr('href')
        else:
            return next_href[0]

    def get_next_page_url(self, response):
        return self.get_npage_url(response, page_a=2)

    def get_prev_page_url(self, response):
        return self.get_npage_url(response, page_a=0)
