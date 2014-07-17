# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import re
import urlparse
import redis

from pyquery import PyQuery as PQ

from scrapy.spider import Spider
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
    start_urls = [
        "http://www.86696.cc/booktopallvisit/0/1.html",
        "http://www.86696.cc/modules/article/toplist.php?sort=monthvisit"
    ]

    def is_pass_url(self, url):
        for i in PASS_URL:
            if i in url:
                return True
        return False

    def parse(self, response):
        url = response.url
        sel = Selector(response)
        jQ = PQ(response.body_as_unicode())
        #书页
        if BOOK_INFO_URL_RE.match(url):
            book = BookinfoItem()
            book['origin_url'] = url
            book['title'] = jQ("h1").text()
            book['author'] = jQ("h2").eq(0).text().replace(u"作者：","")
            book['category'] = jQ("h2").eq(2).text().replace(u"所属：","")
            book['info'] = jQ(".msgarea>p").text().replace(" ","\n")
            book['book_number'] = BOOK_INFO_URL_RE.match(url).groupdict()['book_id']
            yield book
            hrefs = sel.css(".button2.white").xpath('a[1]/@href').extract()
            for href in hrefs:
                yield Request(urlparse.urljoin(url,href), callback=self.parse)
        # 书目
        elif BOOK_INDEX_URL_RE.match(url):
            hrefs = sel.xpath("//dl/dd/a/@href").extract()
            for href in hrefs:
                if RC.get(urlparse.urljoin(url, href)):
                    continue
                yield Request(urlparse.urljoin(url,href), callback=self.parse)
        #章节
        elif BOOK_PAGE_URL_RE.match(url):
            page = BookpageItem()
            page['origin_url'] = url
            page['title'] = sel.xpath('//h1/text()').extract()[0]
            page['content'] = jQ('#BookText').text().replace(" ","\n")
            page['book_number'] = BOOK_PAGE_URL_RE.match(url).groupdict()['book_id']
            page['page_number'] = BOOK_PAGE_URL_RE.match(url).groupdict()['page_id']
            next_href = self.get_next_page_url(response)
            prev_href = self.get_prev_page_url(response)
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
            # 爬下一页
            #yield Request(urlparse.urljoin(url,next_href), callback=self.parse)
            # 爬上一页
            #yield Request(urlparse.urljoin(url,prev_href), callback=self.parse)
        # 继续爬行
        else:
            for href in sel.xpath("//a/@href").extract():
                if self.is_pass_url(href):
                    continue
                if not href.startswith('javascript:') and href != '/' and not href.startswith("#"):
                    # print href
                    href = urlparse.urljoin(url,href)
                    if BOOK_PAGE_URL_RE.match(href):
                        continue
                    if RC.get(href):
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

