# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from django.views.generic import TemplateView
from django.http import Http404, HttpResponse
from django.core.paginator import Paginator
from django.views.decorators.cache import cache_page

from .models import Book, BookPage

home = TemplateView.as_view(template_name="book/index.html")


def home(request):
    books = Book.objects.all()
    C = {}
    p = Paginator(books, 30)
    try:
        page = p.page(int(request.GET.get('p', 1)))
    except:
        page = p.page(1)
    C['books'] = page.object_list
    C['pagination'] = page
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
    if page_number == 0:
        raise Http404
    bookpage = get_object_or_404(BookPage, page_number=page_number)
    book = get_object_or_404(Book, book_number=bookpage.book_number)
    C = {}
    C['book'] = book
    C['bookpage'] = bookpage
    return render(request, 'book/bookpage.html', C)
