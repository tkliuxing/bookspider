# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import time
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from django.views.generic import TemplateView
from django.http import Http404, HttpResponse
from django.core.paginator import Paginator
from django.views.decorators.cache import cache_page

from .models import Book, BookPage, BookRank

home = TemplateView.as_view(template_name="book/index.html")


def home(request):
    C = {}
    books = Book.objects.all().order_by('pk')
    if request.GET.get('s',''):
        books = books.filter(title__contains=request.GET['s'])
        C['search'] = True
    if request.GET.get('a',''):
        books = Book.objects.filter(author=request.GET['a'])
        C['author'] = request.GET['a']
        if not books:
            raise Http404
    p = Paginator(books, 30)
    try:
        page = p.page(int(request.GET.get('p', 1)))
    except:
        page = p.page(1)
    C['books'] = page.object_list
    C['pagination'] = page
    return render(request, 'book/index.html', C)

def category(request, category):
    CATEGORYS = {
        "a":"侦探推理",
        "b":"武侠修真",
        "c":"网游动漫",
        "d":"历史军事",
        "e":"都市言情",
        "f":"散文诗词",
        "g":"玄幻魔法",
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
    return render(request, 'book/index.html', C)


def bookindex(request, book_id=0):
    if book_id == 0:
        raise Http404
    book = get_object_or_404(Book, pk=book_id)
    bookpages = BookPage.objects.filter(book_number=book.book_number).order_by('page_number')
    C = {}
    C['book'] = book
    C['bookpages'] = bookpages
    return render(request, 'book/bookindex.html', C)

@cache_page(60*60)
def bookindexajax(request, book_id=0):
    if book_id == 0:
        raise Http404
    book = get_object_or_404(Book, pk=book_id)
    bookpages = BookPage.objects.filter(book_number=book.book_number).order_by('page_number')
    C = {'bookpages': bookpages}
    data = render_to_string('book/bookindexajax.html', C)
    return HttpResponse(data)

def bookpage(request, page_number=0):
    if request.GET.get('invert',False):
        request.session['invert'] = not request.session.get('invert', False)
        return HttpResponse('')
    if page_number == 0:
        raise Http404
    bookpage = get_object_or_404(BookPage, page_number=page_number)
    book = get_object_or_404(Book, book_number=bookpage.book_number)
    if request.user.is_authenticated():
        skey = 'time-book-%d'%book.pk
        now = int(time.time())
        timeold = request.session.setdefault(skey,now)
        if (now-timeold) > 21600:
            request.session[skey] = now
            book.get_bookrank().add_point()
        elif now == timeold:
            book.get_bookrank().add_point()
    C = {}
    C['book'] = book
    C['bookpage'] = bookpage
    C['invert'] = request.session.get('invert', False)
    return render(request, 'book/bookpage.html', C)

def bookrank(request):
    C = {}
    model_fields_dict = dict(map(lambda x:(x.name,x), BookRank._meta._field_name_cache))
    model_fields_dict.pop('book')
    sort_key = request.GET.get("s", None)
    if model_fields_dict.has_key(sort_key):
        bookranks = BookRank.objects.all().order_by("-%s" % sort_key, "-all_point", "book__pk")
    else:
        bookranks = BookRank.objects.all().order_by("-all_point", "book__pk")
    p = Paginator(bookranks, 30)
    try:
        page = p.page(int(request.GET.get('p', 1)))
    except:
        page = p.page(1)
    C['bookranks'] = page.object_list
    C['pagination'] = page
    return render(request, 'book/bookrank.html', C)
