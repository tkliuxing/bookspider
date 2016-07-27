# -*- coding: utf-8 -*-
import redis

from django.core.management.base import BaseCommand
from django.core.paginator import Paginator

from booksite.book.models import Book

class Command(BaseCommand):
    args = ''
    help = 'Restore DB\'s BookPage url to Redis server.'

    def handle(self, *args, **options):
        for book in Book.objects.all().order_by('title'):
            print(book.title)
