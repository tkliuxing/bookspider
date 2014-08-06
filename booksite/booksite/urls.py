# -*- coding: utf-8 -*-
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
    url(r'^admin/', include(admin.site.urls)),
    url(r'^usercenter/', include(usercenter_urls)),
    url(r'^login/$', 'booksite.usercenter.views.login_view', name='login'),
    url(r'^logout/$', 'booksite.usercenter.views.logout_view', name='logout'),
    url(r'^captcha/', include('captcha.urls')),
)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)