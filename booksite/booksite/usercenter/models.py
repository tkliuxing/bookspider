# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import AbstractUser

from booksite.book.models import Book, BookPage

class User(AbstractUser):
    '''用户'''
    def __unicode__(self):
        return self.username


class BookMark(models.Model):
    '''书签'''

    user = models.ForeignKey(User, verbose_name=_("用户"))
    book = models.ForeignKey(Book, verbose_name=_("书籍"))
    page = models.ForeignKey(BookPage, verbose_name=_("章节"))
    create_time = models.DateTimeField(auto_now_add=True, auto_now=True)

    class Meta:
        # 一个用户对于一本书只能有一个书签
        unique_together = (
            ('user', 'book'),
        )
        ordering = ['-create_time']
        verbose_name = _('BookMark')
        verbose_name_plural = _('BookMarks')

    def __unicode__(self):
        return "User:%s, Book:%s, Page:%s" % (self.user_id, self.book_id, self.page_id)
