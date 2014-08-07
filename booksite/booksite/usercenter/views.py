# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.http import Http404
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.views import login as auth_loginview
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm

from captcha.fields import CaptchaField

from booksite.book.models import BookPage
from booksite.usercenter.models import BookMark
from booksite.ajax import ajax_success, ajax_error


class MyAuthenticationForm(AuthenticationForm):
    captcha = CaptchaField()


def login_view(request):
    return auth_loginview(
        request,
        template_name="usercenter/login.html",
        authentication_form=MyAuthenticationForm
    )

def logout_view(request):
    auth_logout(request)
    return redirect("/")

@login_required
def bookmark(request):
    C = {}
    C['bookmarks'] = BookMark.objects.filter(user=request.user)
    return render(request, "usercenter/bookmark.html", C)


@login_required
def add_bookmark(request):
    if request.method == 'POST':
        try:
            page = BookPage.objects.get(pk=request.POST.get('pageid','-1'))
        except:
            return ajax_error("章节错误!")
        obj, created = BookMark.objects.get_or_create(
            user=request.user,
            book=page.book,
            defaults={"page": page}
        )
        if not created:
            obj.delete()
            obj = BookMark.objects.create(
                user=request.user,
                book=page.book,
                page=page
            )
        else:
            page.book.get_bookrank().add_fav()
        return ajax_success(data="添加成功!")
    else:
        raise Http404


@login_required
def del_bookmark(request, bookmark_id):
    if request.method == 'POST':
        try:
            bookmark = BookMark.objects.get(pk=bookmark_id, user=request.user)
            book = bookmark.book
            bookmark.delete()
            book.get_bookrank().sub_fav()
        except:
            return ajax_error("无法删除此书签!")
        return ajax_success(data="删除成功!")
    else:
        raise Http404
