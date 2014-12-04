# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import urlparse

from scrapy.item import Item, Field
from scrapy.contrib.djangoitem import DjangoItem

from booksite.book.models import Book, BookPage


class BookinfoItem(DjangoItem):
    django_model = Book


class BookpageItem(DjangoItem):
    django_model = BookPage


class QidianRankItem(Item):
    title = Field()
    time_type = Field()
    vip_click = Field()

    def save(self):
        try:
            book = Book.objects.get(title=self["title"])
        except:
            return False
        else:
            book_rank = book.get_bookrank()
            if self["time_type"] == "a":
                book_rank.all_push = self["vip_click"]
            if self["time_type"] == "m":
                book_rank.mon_push = self["vip_click"]
            if self["time_type"] == "w":
                book_rank.wek_push = self["vip_click"]
            book_rank.save()
            return True

    @staticmethod
    def get_time_type(url):
        TT = {'3': 'a', '2': 'm', '1': 'w'}
        url_obj = urlparse.urlparse(url)
        time_num = urlparse.parse_qs(url_obj.query).get("Time", ['3'])[0]
        return TT.get(time_num, 'a')
