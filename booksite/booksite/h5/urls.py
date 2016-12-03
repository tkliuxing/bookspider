# -*- encoding:utf-8 -*-
from django.conf.urls import url
from .views import (
    bookindex, bookpage,
    index, load,
    search, searchload
)

urlpatterns = [
    url(r'^$', index, name='h5'),
    url(r'^load/$', load, name='load'),
    url(r'^search/$', search, name='search'),
    url(r'^searchload/$', searchload, name='searchload'),
    url(r'^book/(?P<book_id>\d+)/$', bookindex, name='bookindex'),
    url(r'^page/(?P<page_number>\d+)/$', bookpage, name='bookpage'),
]
