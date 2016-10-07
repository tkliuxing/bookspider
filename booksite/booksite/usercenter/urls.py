# -*- encoding:utf-8 -*-
from django.conf.urls import url
from .views import (
    bookmark,
    bookmark_read,
    add_bookmark,
    del_bookmark,
    ChangePWDView
)

urlpatterns = [
    url(r'^bookmark/$', bookmark, name='bookmark'),
    url(r'^bookmark/(?P<bookmark_id>\d+)/read/(?P<page_number>\d+)/$',
        bookmark_read, name='bookmark_read'),
    url(r'^bookmark/add/$', add_bookmark, name='add_bookmark'),
    url(r'^bookmark/(?P<bookmark_id>\d+)/delete/$', del_bookmark, name='del_bookmark'),
    url(r'^changepwd/$', ChangePWDView.as_view(), name='changepwd'),
]
