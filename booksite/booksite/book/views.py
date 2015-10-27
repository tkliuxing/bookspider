# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import time
import random
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from django.template import RequestContext
from django.http import Http404, HttpResponse
from django.core.paginator import Paginator
from django.views.decorators.cache import cache_page
from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django import forms
from pyquery import PyQuery as PQ

from booksite.ajax import ajax_success, ajax_error
from booksite.background.models import FengTui, JingTui
from .models import Book, BookPage, BookRank, KeyValueStorage
from .tasks import update_page, update_book_pic_page


def home(request):
    C = {}
    books = Book.objects.filter(is_deleted=False).order_by('book_number')
    if request.GET.get('s', ''):
        books = books.filter(title__contains=request.GET['s'])
        C['search'] = True
    if request.GET.get('a', ''):
        books = Book.objects.filter(is_deleted=False, author=request.GET['a'])
        C['author'] = request.GET['a']
        if not books:
            raise Http404
    p = Paginator(books, 42)
    pn = int(request.GET.get('p', 1))
    try:
        page = p.page(pn)
    except:
        page = p.page(1)
    if pn == 1 and not request.GET.get('s', '') and not request.GET.get('a', ''):
        ft_books = FengTui().books[:6]
        ft_books += [None] * (6 - len(ft_books))
        C['ft_books'] = ft_books
        jt_books = JingTui().books[:15]
        jt_books += [None] * (15 - len(jt_books))
        C['jt_books'] = jt_books
    C['books'] = page.object_list
    C['pagination'] = page
    return render(request, 'book/index.jade', C)


def mb_index(request):
    C = {}
    books = Book.objects.filter(is_deleted=False).order_by('book_number')
    if request.GET.get('a', ''):
        books = Book.objects.filter(is_deleted=False, author=request.GET['a'])
        C['author'] = request.GET['a']
        if not books:
            raise Http404
    p = Paginator(books, 15)
    page = p.page(1)
    C['books'] = page.object_list
    C['pagination'] = page
    return render(request, 'bookhtml5/base.html', C)


def mb_search(request):
    C = {}
    books = Book.objects.filter(is_deleted=False).order_by('book_number')
    if request.GET.get('s', ''):
        books = books.filter(title__contains=request.GET['s'])
        C['search'] = True
    else:
        books = []
    p = Paginator(books, 15)
    try:
        page = p.page(int(request.GET.get('p', 1)))
    except:
        page = p.page(1)
    C['books'] = page.object_list
    C['pagination'] = page
    return render(request, 'bookhtml5/search.html', C)


def mb_searchload(request):
    C = {}
    books = Book.objects.filter(is_deleted=False).order_by('book_number')
    if request.GET.get('s', ''):
        books = books.filter(title__contains=request.GET['s'])
        C['search'] = True
    else:
        books = []
    p = Paginator(books, 15)
    try:
        page = p.page(int(request.GET.get('p', 1)))
    except:
        page = p.page(1)
    C['books'] = page.object_list
    data = render_to_string('bookhtml5/searchload.html', C)
    return ajax_success(data=data)


def mb_load(request):
    C = {}
    books = Book.objects.filter(is_deleted=False).order_by('book_number')
    p = Paginator(books, 15)
    try:
        page = p.page(int(request.GET.get('p', 1)))
    except:
        page = p.page(1)
    C['books'] = page.object_list
    data = render_to_string('bookhtml5/searchload.html', C)
    return ajax_success(data=data)


def category(request, category):
    CATEGORYS_KV, created = KeyValueStorage.objects.get_or_create(
        key='CATEGORYS',
        defaults={'value': '', 'long_value': ''}
    )
    if created:
        real_categorys = Book.objects.order_by('category').distinct('category').values_list('category', flat=True)
        CATEGORYS_KV.val = {chr(x[0]): x[1] for x in zip(range(97, 123), real_categorys)}
        CATEGORYS_KV.save()
    if category not in CATEGORYS_KV.val:
        raise Http404
    books = Book.objects.filter(is_deleted=False, category=CATEGORYS_KV.val[category])
    C = {}
    p = Paginator(books, 30)
    try:
        page = p.page(int(request.GET.get('p', 1)))
    except:
        page = p.page(1)
    C['books'] = page.object_list
    C['pagination'] = page
    C['category'] = CATEGORYS_KV.val[category]
    C['categorynav'] = "nav%s" % category
    return render(request, 'book/index.jade', C)


@cache_page(60 * 60)
def bookinfo(request, book_id=0):
    if book_id == 0:
        raise Http404
    book = get_object_or_404(Book, pk=book_id, is_deleted=False)
    tuijian = Book.objects.filter(category=book.category)
    tuijian = random.sample(tuijian.values_list("id", flat=True), 5) if tuijian.count() >= 5 else random.sample(
        tuijian.values_list("id", flat=True), tuijian.count())
    tuijian = Book.objects.filter(id__in=tuijian)
    C = {}
    C['book'] = book
    C['tuijian'] = tuijian
    return render(request, 'book/bookinfo.jade', C)


@cache_page(60 * 60)
def bookindex(request, book_id=0):
    if book_id == 0:
        raise Http404
    book = get_object_or_404(Book, pk=book_id, is_deleted=False)
    bookpages = BookPage.objects.filter(book_number=book.book_number).order_by('page_number')
    C = {}
    C['book'] = book
    C['bookpages'] = bookpages
    return render(request, 'book/bookindex.jade', C)


def mb_bookindex(request, book_id=0):
    if book_id == 0:
        raise Http404
    book = get_object_or_404(Book, pk=book_id, is_deleted=False)
    bookpages = BookPage.objects.filter(book_number=book.book_number).order_by('page_number')
    C = {}
    C['book'] = book
    C['bookpages'] = bookpages
    return render(request, 'bookhtml5/bookindex.html', C)


@cache_page(60 * 60)
def bookindexajax(request, book_id=0):
    if book_id == 0:
        raise Http404
    book = get_object_or_404(Book, pk=book_id, is_deleted=False)
    bookpages = BookPage.objects.filter(book_number=book.book_number).order_by('page_number')
    C = {'bookpages': bookpages}
    data = render_to_string('book/bookindexajax.jade', C)
    return HttpResponse(data)


def bookpage(request, page_number=0):
    if request.GET.get('invert', False):
        request.session['invert'] = not request.session.get('invert', False)
        return HttpResponse('')
    if page_number == 0:
        raise Http404
    bookpage = get_object_or_404(BookPage, page_number=page_number)
    book = get_object_or_404(Book, is_deleted=False, book_number=bookpage.book_number)
    # 注册用户的点击数据统计
    if request.user.is_authenticated():
        skey = 'time-book-%d' % book.pk
        now = int(time.time())
        timeold = request.session.setdefault(skey, now)
        if (now - timeold) > 21600:
            request.session[skey] = now
            book.get_bookrank().add_point()
        elif now == timeold:
            book.get_bookrank().add_point()
    C = {}
    C['book'] = book
    C['bookpage'] = bookpage
    C['invert'] = request.session.get('invert', False)
    return render(request, 'book/bookpage.jade', C)


def bookpage_zip(request, path):
    from django.conf import settings
    import os
    media_root = settings.MEDIA_ROOT
    page_path = os.path.join(media_root, 'book/', path)
    page_path = page_path.replace("../", "")
    try:
        content_file = open(page_path + '.gz', 'rb')
        page_content = content_file.read()
    except:
        raise Http404
    finally:
        content_file.close()
    response = HttpResponse(page_content, content_type="text/html; charset=UTF-8", )
    response["Content-Encoding"] = 'gzip'
    return response


def mb_bookpage(request, page_number=0):
    if request.GET.get('invert', False):
        request.session['invert'] = not request.session.get('invert', False)
        return HttpResponse('')
    if page_number == 0:
        raise Http404
    bookpage = get_object_or_404(BookPage, page_number=page_number)
    book = get_object_or_404(Book, is_deleted=False, book_number=bookpage.book_number)
    # 注册用户的点击数据统计
    if request.user.is_authenticated():
        skey = 'time-book-%d' % book.pk
        now = int(time.time())
        timeold = request.session.setdefault(skey, now)
        if (now - timeold) > 21600:
            request.session[skey] = now
            book.get_bookrank().add_point()
        elif now == timeold:
            book.get_bookrank().add_point()
    C = {}
    C['book'] = book
    C['bookpage'] = bookpage
    C['invert'] = request.session.get('invert', False)
    return render(request, 'bookhtml5/bookpage.html', C)


def bookrank(request):
    C = {}
    PREPAGE = 50
    model_fields_dict = dict(map(lambda x: (x.name, x), BookRank._meta._field_name_cache))
    model_fields_dict.pop('book')
    sort_key = request.GET.get("s", None)
    if model_fields_dict.has_key(sort_key):
        bookranks = BookRank.objects.all().order_by("-%s" % sort_key, "-all_point", "book__pk")
    else:
        bookranks = BookRank.objects.all().order_by("-all_point", "book__pk")
    p = Paginator(bookranks, PREPAGE)
    try:
        page = p.page(int(request.GET.get('p', 1)))
    except:
        page = p.page(1)
    C['bookranks'] = page.object_list
    C['pagination'] = page
    C['number_base'] = PREPAGE * (page.number - 1)
    return render(request, 'book/bookrank.jade', C)


@cache_page(60 * 60)
def booknews(request):
    """最近更新列表"""
    C = {}
    TOTALPAGE = 20
    PREPAGE = 20
    books = Book.objects.order_by(
        "-last_update").filter(is_deleted=False, last_update__isnull=False)[:TOTALPAGE * PREPAGE]
    p = Paginator(books, PREPAGE)
    try:
        page = p.page(int(request.GET.get('p', 1)))
    except:
        page = p.page(1)
    C['books'] = page.object_list
    C['pagination'] = page
    return render(request, 'book/booknews.jade', C)


def load_nall_page(request, page_id=0):
    bookpage = BookPage.objects.get(pk=page_id)
    book = Book.objects.get(is_deleted=False, book_number=bookpage.book_number)
    bookpages = []
    next_page_number = bookpage.next_number
    # 使用链式获取比排序后截取快
    for i in range(10):
        try:
            next_page = BookPage.objects.get(page_number=next_page_number)
        except:
            break
        else:
            bookpages.append(next_page)
            next_page_number = next_page.next_number

    data = render_to_string(
        'book/pagecontent.jade',
        {
            'bookpages': bookpages,
            'book': book,
            'invert': request.session.get('invert', False),
        }
    )
    return ajax_success(data)


@login_required
def page_fix_pic(request, page_id=0):
    if not request.user.is_superuser:
        raise Http404
    bookpage = get_object_or_404(BookPage, pk=page_id)
    title = bookpage.title
    book_title = bookpage.book.title
    update_page.delay(page_id, book_title, title)
    cache.set("pagetask-%s" % page_id, 'RUN', 600)
    return ajax_success()


@login_required
def page_task_check(request, page_id=0):
    if not request.user.is_superuser:
        raise Http404
    get_object_or_404(BookPage, pk=page_id)
    status = cache.get("pagetask-%s" % page_id)
    if status:
        return ajax_success(data={'status': status})
    else:
        return ajax_error('未知的任务')


@login_required
def book_fix_pic(request, book_id=0):
    if not request.user.is_superuser:
        raise Http404
    book = get_object_or_404(Book, pk=book_id, is_deleted=False)
    update_book_pic_page.delay(book.book_number, 200)
    return ajax_success()


@login_required
def edit_line(request):
    if not request.user.is_superuser:
        raise Http404

    class CheckForm(forms.Form):
        pagenum = forms.ModelChoiceField(queryset=BookPage.objects.all())
        linenum = forms.IntegerField(min_value=0)
        pageline = forms.CharField(max_length=2000)
    if request.method != "POST":
        raise HttpResponse(status_code=405)
    form = CheckForm(request.POST)
    if form.is_valid():
        import re
        new_lines = re.sub(r"\n+", '\n', form.cleaned_data["pageline"], flags=re.S).split('\n')
        page = form.cleaned_data["pagenum"]
        page_contents = BookPage.content_text(page.get_content()).split('\n')
        line_number = form.cleaned_data["linenum"]
        # # Diff信息
        # import difflib
        # content_line = page_contents[line_number]
        # dif = difflib.Differ()
        # diffline = ("\n".join(
        #     list(dif.compare(content_line.splitlines(1), form.cleaned_data["pageline"].splitlines(1)))
        # )).replace(" ", "　").replace("-", "－").replace("?", "？").replace("+", "＋")
        # print diffline
        page_contents[line_number] = form.cleaned_data["pageline"]
        page_contents = page_contents[:line_number] + new_lines + page_contents[line_number + 1:]
        new_content = BookPage.content_html("\n".join(page_contents))
        page.set_content(new_content)
        return ajax_success(new_content)
    else:
        return ajax_error(form.errors.as_json())


@login_required
def del_line(request, page_id=0):
    if request.method != "POST":
        raise HttpResponse(status_code=405)
    if not request.user.is_superuser:
        raise Http404
    page = get_object_or_404(BookPage, pk=page_id)
    page_contents = BookPage.content_text(page.get_content()).split('\n')
    try:
        page_contents.pop(int(request.POST["ln"]))
    except:
        return ajax_error("非法数据!")
    new_content = BookPage.content_html("\n".join(page_contents))
    page.set_content(new_content)
    return ajax_success(new_content)
