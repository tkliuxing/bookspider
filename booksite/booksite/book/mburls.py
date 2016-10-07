# -*- encoding:utf-8 -*-
from django.conf.urls import url
from .views import (
    mb_bookindex, mb_bookpage,
    mb_index, mb_load,
    mb_search, mb_searchload
)

urlpatterns = [
    url(r'^$', mb_index, name='mb'),
    url(r'^load/$', mb_load, name='mb_load'),
    url(r'^search/$', mb_search, name='mb_search'),
    url(r'^searchload/$', mb_searchload, name='mb_searchload'),
    url(r'^book/(?P<book_id>\d+)/$', mb_bookindex, name='mb_bookindex'),
    url(r'^page/(?P<page_number>\d+)/$', mb_bookpage, name='mb_bookpage'),
]
