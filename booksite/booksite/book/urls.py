# -*- encoding:utf-8 -*-

from django.conf.urls import url

from .views import (
    home, category, bookrank, booknews,
    bookindex, bookpage, bookinfo, bookindexajax,
    load_nall_page, page_fix_pic, book_fix_pic,
    page_task_check, edit_line, del_line
)

urlpatterns = [
    url(r'^$', home, name='home'),
    url(r'^fenlei/(?P<category>[a-z])/$', category, name='category'),
    url(r'^bookrank/$', bookrank, name='bookrank'),
    url(r'^booknews/$', booknews, name='booknews'),
    url(r'^book/(?P<book_id>\d+)/$', bookindex, name='bookindex'),
    url(r'^bookinfo/(?P<book_id>\d+)/$', bookinfo, name='bookinfo'),
    url(r'^bookindex/(?P<book_id>\d+)/$', bookindexajax, name='bookindexajax'),
    url(r'^page/(?P<page_number>\d+)/$', bookpage, name='bookpage'),

    url(r'^nallpage/(?P<page_id>\d+)/$', load_nall_page, name='nallpage'),
    url(r'^fixpic/page/(?P<page_id>\d+)/$', page_fix_pic, name='pagefixpic'),
    url(r'^fixpic/book/(?P<book_id>\d+)/$', book_fix_pic, name='bookfixpic'),
    url(r'^taskcheck/page/(?P<page_id>\d+)/$', page_task_check, name='pagetaskcheck'),
    url(r'^lineupdate/$', edit_line, name="lineupdate"),
    url(r'^lineremove/(?P<page_id>\d+)/$', del_line, name="del_line"),
]
