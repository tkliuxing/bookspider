# -*- coding: utf-8 -*-
from __future__ import unicode_literals
# import re
import urlparse
import urllib
# import redis

from pyquery import PyQuery as PQ

from scrapy.spider import Spider
# from scrapy.selector import Selector
from scrapy.http import Request

from bookspider.items import QidianRankItem

# RC = redis.Redis()


class QidianRankSpider(Spider):
    name = "qidianrank"
    allowed_domains = ["top.qidian.com"]
    start_urls = [
        "http://top.qidian.com/Book/TopDetail.aspx?TopType=1&Time=3&PageIndex=1",
        "http://top.qidian.com/Book/TopDetail.aspx?TopType=1&Time=3&PageIndex=10",
        "http://top.qidian.com/Book/TopDetail.aspx?TopType=1&Time=3&PageIndex=20",
        "http://top.qidian.com/Book/TopDetail.aspx?TopType=1&Time=3&PageIndex=30",
        "http://top.qidian.com/Book/TopDetail.aspx?TopType=1&Time=3&PageIndex=40",
    ]

    # def is_pass_url(self, url):
    #     for i in PASS_URL:
    #         if i in url:
    #             return True
    #     return False

    def parse(self, response):
        url = response.url
        # sel = Selector(response)
        jQ = PQ(response.body_as_unicode())
        for i in jQ("#list1 tr"):
            elem = jQ(i)
            title = elem.find("td").eq(2).find("a").eq(0).text()
            if title:
                try:
                    click = int(elem.find("td").eq(3).text())
                except:
                    continue
                else:
                    item = QidianRankItem()
                    item["title"] = title
                    item["vip_click"] = click
                    yield item
        url_obj = urlparse.urlparse(url)
        page_num = str(
            int(urlparse.parse_qs(url_obj.query).get("PageIndex", ['0'])[0]) + 1
        )
        if page_num == "50":
            yield Request(url, callback=self.parse)
        else:
            new_qs = urllib.urlencode({
                "PageIndex": page_num,
                "Time": '3',
                "TopType": '1',
            })
            new_url = urlparse.urlunparse([
                url_obj.scheme,
                url_obj.netloc,
                url_obj.path,
                url_obj.params,
                new_qs,
                url_obj.fragment
            ])
            yield Request(new_url, callback=self.parse)
