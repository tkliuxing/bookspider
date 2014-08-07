# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.db import connection
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _


class Book(models.Model):
    origin_url = models.TextField()
    title = models.CharField(max_length=100, blank=True)
    author = models.CharField(max_length=100, blank=True)
    category = models.CharField(max_length=20, blank=True)
    info = models.TextField(blank=True)
    book_number = models.IntegerField(db_index=True, unique=True)

    class Meta:
        ordering = ['book_number']

    @property
    def info_html(self):
        s = u"\n\n".join(self.info.split("\n"))
        return s

    def get_absolute_url(self):
        return reverse('bookindex', args=[str(self.id)])

    def get_bookrank(self):
        return BookRank.objects.get_or_create(book=self)[0]


class BookPage(models.Model):
    origin_url = models.TextField()
    title = models.CharField(max_length=100, blank=True)
    content = models.TextField(blank=True)
    book_number = models.IntegerField(db_index=True)
    page_number = models.IntegerField(db_index=True, unique=True)
    next_number = models.IntegerField(default=0, null=True)
    prev_number = models.IntegerField(default=0, null=True)

    class Meta:
        ordering = ['book_number', 'page_number']

    @property
    def title_html(self):
        book_title = Book.objects.get(book_number=self.book_number).title
        s = self.title.split(" ")[1:]
        title = " ".join(s)
        if title.startswith(book_title):
            title = title[len(book_title):]
        return title

    @property
    def content_html(self):
        replace_list = [
            ("&1t;", "<"),
            ("大6", "大陆"),
            ("&ldqo;", "“"),
            ("&rdqo;", "”"),
        ]
        changed = False
        for rep in replace_list:
            if rep[0] in self.content:
                self.content = self.content.replace(rep[0], rep[1])
                changed = True
        if changed:
            self.save()
        c = self.content.replace('\n', '\n\n')
        return c

    @property
    def book(self):
        return Book.objects.get(book_number=self.book_number)

    def get_absolute_url(self):
        return reverse('bookpage', args=[str(self.page_number)])


class BookRank(models.Model):
    class Meta:
        verbose_name = _('BookRank')
        verbose_name_plural = _('BookRanks')

    book = models.OneToOneField(Book)

    all_point = models.IntegerField(_("总点击"), default=0)
    mon_point = models.IntegerField(_("月点击"), default=0)
    wek_point = models.IntegerField(_("周点击"), default=0)

    all_push = models.IntegerField(_("周推荐"), default=0)
    mon_push = models.IntegerField(_("周推荐"), default=0)
    wek_push = models.IntegerField(_("周推荐"), default=0)

    all_fav = models.IntegerField(_("总收藏"), default=0)

    def add_point(self):
        cursor = connection.cursor()
        cursor.execute("\
            update book_bookrank \
            set all_point=all_point+1,mon_point=mon_point+1,wek_point=wek_point+1 \
            where id=%s;", [self.pk])

    def add_push(self):
        cursor = connection.cursor()
        cursor.execute("\
            update book_bookrank \
            set all_push=all_push+1,mon_push=mon_push+1,wek_push=wek_push+1 \
            where id=%s;", [self.pk])

    def add_fav(self):
        cursor = connection.cursor()
        cursor.execute("\
            update book_bookrank \
            set all_fav=all_fav+1 \
            where id=%s;", [self.pk])

    def sub_fav(self):
        cursor = connection.cursor()
        cursor.execute("\
            update book_bookrank \
            set all_fav=all_fav-1 \
            where id=%s;", [self.pk])
