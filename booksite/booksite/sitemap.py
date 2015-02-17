# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from booksite.baidusitemap import BaiduSitemap
from booksite.book.models import Book

class BookSitemaps(BaiduSitemap):
    changefreq = 'daily'
    priority = 0.5

    def items(self):
        return Book.objects.order_by("-last_update").filter(last_update__isnull=False)

    def lastmod(self , obj):
        return obj.last_update

    def bookrank_url(self, obj):
        return '/bookrank/'

    def booknews_url(self, obj):
        return '/booknews/'

    def fenlei_xuanhuan_url(self, obj):
        return '/fenlei/g/'
    def fenlei_zhentan_url(self, obj):
        return '/fenlei/a/'
    def fenlei_wuxia_url(self, obj):
        return '/fenlei/b/'
    def fenlei_wangyou_url(self, obj):
        return '/fenlei/c/'
    def fenlei_lishi_url(self, obj):
        return '/fenlei/d/'
    def fenlei_dushi_url(self, obj):
        return '/fenlei/e/'
    def fenlei_sanwen_url(self, obj):
        return '/fenlei/f/'

