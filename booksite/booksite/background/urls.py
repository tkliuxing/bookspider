# -*- encoding:utf-8 -*-
from django.conf.urls import url
from .views import (
    index,
    replace,
    delete_rule, edit_rule, apply_rule,
    replace_page, replace_book,
    tuijian, fengtui_create, jingtui_create,
    del_tuijian,
    book_search, book_jx, book_ft, book_jt,
    book_jiuzhenggengxin,
    book_page_next_zipper,
    get_new_book,
)

urlpatterns = [
    url(r'^$', index, name="home"),
    url(r'^replace/$', replace, name="replace"),
    url(r'^replace/delete/(?P<pk>\d+)/$', delete_rule, name="delete_rule"),
    url(r'^replace/edit/(?P<pk>\d+)/$', edit_rule, name="edit_rule"),
    url(r'^replace/apply/(?P<pk>\d+)/$', apply_rule, name="apply_rule"),
    url(r'^replace/page/$', replace_page, name="replace_page"),
    url(r'^replace/book/$', replace_book, name="replace_book"),
    url(r'^tuijian/$', tuijian, name="tuijian"),
    url(r'^tuijian/create/fengtui/$', fengtui_create, name="fengtui_create"),
    url(r'^tuijian/create/jingtui/$', jingtui_create, name="jingtui_create"),
    url(r'^tuijian/delete/(?P<model>ft|jt)/(?P<book_id>\d+)/$', del_tuijian, name="del_tuijian"),
    url(r'^booksearch/$', book_search, name="book_search"),
    url(r'^booksearch/jx/$', book_jx, name="book_jx"),
    url(r'^booksearch/ft/$', book_ft, name="book_ft"),
    url(r'^booksearch/jt/$', book_jt, name="book_jt"),
    url(r'^booksearch/jxall/$', book_jiuzhenggengxin, name="book_jiuzhenggengxin"),
    url(r'^booksearch/pagezipper/$', book_page_next_zipper, name="book_page_next_zipper"),
    url(r'^newbook/$', get_new_book, name="newbook"),
]
