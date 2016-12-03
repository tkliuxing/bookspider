# -*- encoding:utf-8 -*-
import time
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from django.http import Http404, HttpResponse
from django.core.paginator import Paginator

from booksite.ajax import ajax_success, ajax_error
from booksite.book.models import Book, BookPage


def index(request):
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
    return render(request, 'h5/base.html', C)


def search(request):
    C = {}
    books = Book.objects.filter(is_deleted=False).order_by('book_number')
    if request.GET.get('s', ''):
        books = books.filter(title__contains=request.GET['s'].strip())
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
    return render(request, 'h5/search.html', C)


def searchload(request):
    C = {}
    books = Book.objects.filter(is_deleted=False).order_by('book_number')
    if request.GET.get('s', ''):
        books = books.filter(title__contains=request.GET['s'].strip())
        C['search'] = True
    else:
        books = []
    p = Paginator(books, 15)
    try:
        page = p.page(int(request.GET.get('p', 1)))
    except:
        page = p.page(1)
    C['books'] = page.object_list
    data = render_to_string('h5/searchload.html', C)
    return ajax_success(data=data)


def load(request):
    C = {}
    books = Book.objects.filter(is_deleted=False).order_by('book_number')
    p = Paginator(books, 15)
    try:
        page = p.page(int(request.GET.get('p', 1)))
    except:
        page = p.page(1)
    C['books'] = page.object_list
    data = render_to_string('h5/searchload.html', C)
    return ajax_success(data=data)


def bookindex(request, book_id=0):
    if book_id == 0:
        raise Http404
    book = get_object_or_404(Book, pk=book_id, is_deleted=False)
    bookpages = BookPage.objects.filter(book_number=book.book_number).order_by('page_number')
    C = {}
    C['book'] = book
    C['bookpages'] = bookpages
    return render(request, 'h5/bookindex.html', C)


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
    return render(request, 'h5/bookpage.html', C)
