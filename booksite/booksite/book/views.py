# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import time
import difflib
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from django.template import RequestContext
from django.http import Http404, HttpResponse
from django.core.paginator import Paginator
from django.views.decorators.cache import cache_page
from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django import forms

from booksite.ajax import ajax_success, ajax_error
from booksite.background.models import FengTui, JingTui
from .models import Book, BookPage, BookRank
from .tasks import update_page, update_book_pic_page


def home(request):
    C = {}
    books = Book.objects.all().order_by('book_number')
    if request.GET.get('s', ''):
        books = books.filter(title__contains=request.GET['s'])
        C['search'] = True
    if request.GET.get('a', ''):
        books = Book.objects.filter(author=request.GET['a'])
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
    books = Book.objects.all().order_by('book_number')
    if request.GET.get('a', ''):
        books = Book.objects.filter(author=request.GET['a'])
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
    books = Book.objects.all().order_by('book_number')
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
    print page.paginator.num_pages
    return render(request, 'bookhtml5/search.html', C)


def mb_searchload(request):
    C = {}
    books = Book.objects.all().order_by('book_number')
    if request.GET.get('s', ''):
        books = books.filter(title__contains=request.GET['s'])
        C['search'] = True
    else:
        books = []
    print request.GET.get('s', '')
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
    books = Book.objects.all().order_by('book_number')
    p = Paginator(books, 15)
    try:
        page = p.page(int(request.GET.get('p', 1)))
    except:
        page = p.page(1)
    C['books'] = page.object_list
    data = render_to_string('bookhtml5/searchload.html', C)
    return ajax_success(data=data)


def category(request, category):
    CATEGORYS = {
        "a": "侦探推理",
        "b": "武侠修真",
        "c": "网游动漫",
        "d": "历史军事",
        "e": "都市言情",
        "f": "散文诗词",
        "g": "玄幻魔法",
    }
    if category not in CATEGORYS:
        raise Http404
    books = Book.objects.filter(category=CATEGORYS[category])
    C = {}
    p = Paginator(books, 30)
    try:
        page = p.page(int(request.GET.get('p', 1)))
    except:
        page = p.page(1)
    C['books'] = page.object_list
    C['pagination'] = page
    C['category'] = CATEGORYS[category]
    C['categorynav'] = "nav%s" % category
    return render(request, 'book/index.jade', C)

@cache_page(60*60)
def bookindex(request, book_id=0):
    if book_id == 0:
        raise Http404
    book = get_object_or_404(Book, pk=book_id)
    bookpages = BookPage.objects.filter(book_number=book.book_number).order_by('page_number')
    C = {}
    C['book'] = book
    C['bookpages'] = bookpages
    return render(request, 'book/bookindex.jade', C)


def mb_bookindex(request, book_id=0):
    if book_id == 0:
        raise Http404
    book = get_object_or_404(Book, pk=book_id)
    bookpages = BookPage.objects.filter(book_number=book.book_number).order_by('page_number')
    C = {}
    C['book'] = book
    C['bookpages'] = bookpages
    return render(request, 'bookhtml5/bookindex.html', C)


@cache_page(60*60)
def bookindexajax(request, book_id=0):
    if book_id == 0:
        raise Http404
    book = get_object_or_404(Book, pk=book_id)
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
    book = get_object_or_404(Book, book_number=bookpage.book_number)
    # 注册用户的点击数据统计
    if request.user.is_authenticated():
        skey = 'time-book-%d' % book.pk
        now = int(time.time())
        timeold = request.session.setdefault(skey, now)
        if (now-timeold) > 21600:
            request.session[skey] = now
            book.get_bookrank().add_point()
        elif now == timeold:
            book.get_bookrank().add_point()
    C = {}
    C['book'] = book
    C['bookpage'] = bookpage
    C['invert'] = request.session.get('invert', False)
    return render(request, 'book/bookpage.jade', C)


def mb_bookpage(request, page_number=0):
    if request.GET.get('invert', False):
        request.session['invert'] = not request.session.get('invert', False)
        return HttpResponse('')
    if page_number == 0:
        raise Http404
    bookpage = get_object_or_404(BookPage, page_number=page_number)
    book = get_object_or_404(Book, book_number=bookpage.book_number)
    # 注册用户的点击数据统计
    if request.user.is_authenticated():
        skey = 'time-book-%d' % book.pk
        now = int(time.time())
        timeold = request.session.setdefault(skey, now)
        if (now-timeold) > 21600:
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
    C['number_base'] = PREPAGE*(page.number-1)
    return render(request, 'book/bookrank.jade', C)


@cache_page(60 * 60)
def booknews(request):
    """最近更新列表"""
    C = {}
    TOTALPAGE = 20
    PREPAGE = 20
    books = Book.objects.order_by("-last_update").filter(last_update__isnull=False)[:TOTALPAGE*PREPAGE]
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
    book = Book.objects.get(book_number=bookpage.book_number)
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
        },
        context_instance=RequestContext(request)
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
    book = get_object_or_404(Book, pk=book_id)
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
        page = form.cleaned_data["pagenum"]
        page_contents = page.content.split("\n")
        line_number = form.cleaned_data["linenum"]
        for i, e in enumerate(page_contents):
            if i == line_number:
                dif = difflib.Differ()
                diffline = ("\n".join(
                    list(dif.compare(e.splitlines(1), form.cleaned_data["pageline"].splitlines(1)))
                )
                ).replace(" ", "　").replace("-", "－").replace("?", "？").replace("+", "＋")
                repr(diffline)
                # print diffline
                page_contents[i] = form.cleaned_data["pageline"]
        page.content = "\n".join(page_contents)
        page.save()
        return ajax_success(form.cleaned_data["pageline"])
    else:
        return ajax_error(form.errors.as_json())


@login_required
def del_line(request, page_id=0):
    if request.method != "POST":
        raise HttpResponse(status_code=405)
    if not request.user.is_superuser:
        raise Http404
    page = get_object_or_404(BookPage, pk=page_id)
    page_contents = page.content.split("\n")
    try:
        page_contents.pop(int(request.POST["ln"]))
    except:
        return ajax_error("非法数据!")
    page.content = "\n".join(page_contents)
    page.save()
    return ajax_success()
