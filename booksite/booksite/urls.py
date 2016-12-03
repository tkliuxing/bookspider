# -*- coding: utf-8 -*-
import django.contrib.auth.views
from django.contrib.sitemaps import views as sitemap_views
# from django.views.generic.base import TemplateView
from django.conf.urls import include, url
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin

from booksite.usercenter.views import (
    login_view, signup, logout_view
)
from booksite.sitemap import BookSitemaps
admin.autodiscover()

sitemaps = {
    'books': BookSitemaps()
}

html5_urls = [
    url(r'^', include('booksite.book.mburls')),
    url(r'^account/', include('booksite.usercenter.mburls')),
]

password_reset_urls = [
    url(r'^$', django.contrib.auth.views.password_reset,
       {'template_name': 'usercenter/password_reset_form.html',
        'email_template_name': 'usercenter/password_reset_email.html',}, name='password_reset'),
    url(r'^done/$', django.contrib.auth.views.password_reset_done,
        {'template_name': 'usercenter/password_reset_done.html'}, name='password_reset_done'),
    url(r'^confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>.+)/$', django.contrib.auth.views.password_reset_confirm,
        {'template_name': 'usercenter/password_reset_confirm.html'}, name='password_reset_confirm'),
    url(r'^complete/$', django.contrib.auth.views.password_reset_complete,
        {'template_name': 'usercenter/password_reset_complete.html'}, name='password_reset_complete'),
]

urlpatterns = [
    url(r'', include('booksite.book.urls')),
    url(r'^comments/', include('django_comments.urls')),

    url(r'^sitemap.xml$', sitemap_views.sitemap, {'sitemaps': sitemaps}),
    url(r'^robots.txt', include('robots.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^usercenter/', include('booksite.usercenter.urls')),
    url(r'^login/$', login_view, name='login'),
    url(r'^signup/$', signup, name='signup'),
    url(r'^logout/$', logout_view, name='logout'),
    url(r'^captcha/', include('captcha.urls')),

    url(r'^resetpassword/', include(password_reset_urls)),

    url(r'^mobile/', include(html5_urls)),

    url(r'^bbg/', include('booksite.background.urls', namespace='bbg', app_name='booksite.background')),
]


if settings.DEBUG:
    import booksite.book.views
    urlpatterns += [url(r'^media/book/(?P<path>.*)$', booksite.book.views.bookpage_zip, name='zippage')]
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
