# -*- coding: utf-8 -*-
from django.shortcuts import render
from booksite.book.models import Book
from .models import ReplaceRule
import json


def index(request):
    C = {}
    CATEGORYS = {
        "a": "侦探推理",
        "b": "武侠修真",
        "c": "网游动漫",
        "d": "历史军事",
        "e": "都市言情",
        "f": "散文诗词",
        "g": "玄幻魔法",
    }.values()
    book_count = Book.objects.all().count()
    category_data = [
        [c, Book.objects.filter(category=c).count()] for c in CATEGORYS
    ]
    C['category_data'] = json.dumps(category_data)
    C['book_count'] = book_count
    return render(request, "background/index.html", C)


def replace(request):
    C = {}
    replace_rule = ReplaceRule.all()
    C['replace_rule'] = replace_rule
    return render(request, "background/replace.html", C)
