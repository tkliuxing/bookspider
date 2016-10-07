# -*- encoding:utf-8 -*-
from django.conf.urls import url
from .views import (
    mb_login, mb_logout, mb_bookmark
)

urlpatterns = [
    url(r'^login/$', mb_login, name='mb_login'),
    url(r'^logout/$', mb_logout, name='mb_logout'),
    url(r'^bookmark/$', mb_bookmark, name='mb_bookmark'),
]
