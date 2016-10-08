# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.sitemaps import Sitemap
from booksite.book.models import Book

class BookSitemaps(Sitemap):
    changefreq = 'hourly'
    priority = 0.5

    def items(self):
        return Book.objects.order_by("-last_update").filter(last_update__isnull=False)[:100]

    def lastmod(self , obj):
        return obj.last_update
