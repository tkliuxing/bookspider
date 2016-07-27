# -*- coding: utf-8 -*-
from optparse import make_option
from django.core.management.base import BaseCommand, CommandError
from django.core.paginator import Paginator
from django.utils.encoding import force_unicode

from booksite.book.tasks import get_new_book_with_book_name

class Command(BaseCommand):
    help = 'Get new book from 86696.cc with book title.'
    args = '<book_title book_title ...>'

    def handle(self, *args, **options):
        if not args:
            raise CommandError('Book title does not given!')
        # self.stdout.write(options['title'])
        for book_title in args:
            book_title = force_unicode(book_title)
            get_new_book_with_book_name(book_title)
            self.stdout.write('%s book done!' % book_title)
        self.stdout.write('\nAll url restored!')
