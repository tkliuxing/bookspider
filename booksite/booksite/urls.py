# -*- coding: utf-8 -*-
# from django.views.generic.base import TemplateView
from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from booksite.usercenter.views import ChangePWDView
admin.autodiscover()

usercenter_urls = patterns('booksite.usercenter.views',
    url(r'^bookmark/$', 'bookmark', name='bookmark'),
    url(r'^bookmark/add/$', 'add_bookmark', name='add_bookmark'),
    url(r'^bookmark/(?P<bookmark_id>\d+)/delete/$', 'del_bookmark', name='del_bookmark'),
    url(r'^changepwd/$', ChangePWDView.as_view(), name='changepwd'),
)

html5_urls = patterns('',
    url(r'^$', 'booksite.book.views.mb_index', name='mb'),
    url(r'^load/$', 'booksite.book.views.mb_load', name='mb_load'),
    url(r'^search/$', 'booksite.book.views.mb_search', name='mb_search'),
    url(r'^searchload/$', 'booksite.book.views.mb_searchload', name='mb_searchload'),
    url(r'^login/$', 'booksite.usercenter.views.mb_login', name='mb_login'),
    url(r'^logout/$', 'booksite.usercenter.views.mb_logout', name='mb_logout'),
    url(r'^bookmark/$', 'booksite.usercenter.views.mb_bookmark', name='mb_bookmark'),
    url(r'^book/(?P<book_id>\d+)/$', 'booksite.book.views.mb_bookindex', name='mb_bookindex'),
    url(r'^page/(?P<page_number>\d+)/$', 'booksite.book.views.mb_bookpage', name='mb_bookpage'),
)

background_urls = patterns('booksite.background.views',
    url(r'^$', 'index', name="home"),
    url(r'^replace/$', 'replace', name="replace"),
    url(r'^replace/delete/(?P<pk>\d+)/$', 'delete_rule', name="delete_rule"),
    url(r'^replace/edit/(?P<pk>\d+)/$', 'edit_rule', name="edit_rule"),
    url(r'^replace/apply/(?P<pk>\d+)/$', 'apply_rule', name="apply_rule"),
    url(r'^replace/page/$', 'replace_page', name="replace_page"),
    url(r'^replace/book/$', 'replace_book', name="replace_book"),
)

password_reset_urls = patterns('',
    url(r'^$',
        'django.contrib.auth.views.password_reset',
        {
            'template_name': 'usercenter/password_reset_form.html',
            'email_template_name': 'usercenter/password_reset_email.html',
        },
        name='password_reset'
    ),
    url(r'^done/$',
        'django.contrib.auth.views.password_reset_done',
        {'template_name': 'usercenter/password_reset_done.html'},
        name='password_reset_done'
    ),
    url(r'^confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>.+)/$',
        'django.contrib.auth.views.password_reset_confirm',
        {'template_name': 'usercenter/password_reset_confirm.html'},
        name='password_reset_confirm'
    ),
    url(r'^complete/$',
        'django.contrib.auth.views.password_reset_complete',
        {'template_name': 'usercenter/password_reset_complete.html'},
        name='password_reset_complete'
    ),
)

urlpatterns = patterns('',
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
    url(r'^lineupdate/$', 'booksite.book.views.edit_line', name="lineupdate"),
    url(r'^lineremove/(?P<page_id>\d+)/$', 'booksite.book.views.del_line', name="del_line"),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^usercenter/', include(usercenter_urls)),
    url(r'^login/$', 'booksite.usercenter.views.login_view', name='login'),
    url(r'^signup/$', 'booksite.usercenter.views.signup', name='signup'),
    url(r'^logout/$', 'booksite.usercenter.views.logout_view', name='logout'),
    url(r'^captcha/', include('captcha.urls')),

    url(r'^resetpassword/', include(password_reset_urls)),

    url(r'^mobile/', include(html5_urls)),

    url(r'^bbg/', include(background_urls, namespace='bbg', app_name='booksite.background')),
)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
