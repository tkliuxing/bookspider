# -*- coding: utf-8 -*-
# from django.views.generic.base import TemplateView
from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
admin.autodiscover()

usercenter_urls = patterns('booksite.usercenter.views',
    url(r'^bookmark/$', 'bookmark', name='bookmark'),
    url(r'^bookmark/add/$', 'add_bookmark', name='add_bookmark'),
    url(r'^bookmark/(?P<bookmark_id>\d+)/delete/$', 'del_bookmark', name='del_bookmark'),
)

html5_urls = patterns('',
    url(r'^$', 'booksite.book.views.mb_index', name='mb'),
    url(r'^login/$', 'booksite.usercenter.views.mb_login', name='mb_login'),
    url(r'^logout/$', 'booksite.usercenter.views.mb_logout', name='mb_logout'),
    url(r'^bookmark/$', 'booksite.usercenter.views.mb_bookmark', name='mb_bookmark'),
    url(r'^book/(?P<book_id>\d+)/$', 'booksite.book.views.mb_bookindex', name='mb_bookindex'),
    url(r'^page/(?P<page_number>\d+)/$', 'booksite.book.views.mb_bookpage', name='mb_bookpage'),
)

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'booksite.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', 'booksite.book.views.home', name='home'),
    url(r'^fenlei/(?P<category>[a-g])/$', 'booksite.book.views.category', name='category'),
    url(r'^bookrank/$', 'booksite.book.views.bookrank', name='bookrank'),
    url(r'^book/(?P<book_id>\d+)/$', 'booksite.book.views.bookindex', name='bookindex'),
    url(r'^bookindex/(?P<book_id>\d+)/$', 'booksite.book.views.bookindexajax', name='bookindexajax'),
    url(r'^page/(?P<page_number>\d+)/$', 'booksite.book.views.bookpage', name='bookpage'),

    url(r'^nallpage/(?P<page_id>\d+)/$', 'booksite.book.views.load_nall_page', name='nallpage'),
    url(r'^fixpic/page/(?P<page_id>\d+)/$', 'booksite.book.views.page_fix_pic', name='pagefixpic'),
    url(r'^fixpic/book/(?P<book_id>\d+)/$', 'booksite.book.views.book_fix_pic', name='bookfixpic'),
    url(r'^taskcheck/page/(?P<page_id>\d+)/$', 'booksite.book.views.page_task_check', name='pagetaskcheck'),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^usercenter/', include(usercenter_urls)),
    url(r'^login/$', 'booksite.usercenter.views.login_view', name='login'),
    url(r'^signup/$', 'booksite.usercenter.views.signup', name='signup'),
    url(r'^logout/$', 'booksite.usercenter.views.logout_view', name='logout'),
    url(r'^captcha/', include('captcha.urls')),

    url(r'^mobile/', include(html5_urls)),
)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)