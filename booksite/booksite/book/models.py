# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import hashlib
import cPickle as pickle
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
    last_update = models.DateTimeField(auto_now=True, null=True, blank=True, default=None, db_index=True)
    last_page_number = models.IntegerField(default=0, null=True, blank=True)

    class Meta:
        ordering = ['book_number']

    @property
    def info_html(self):
        s = u"\n\n".join(self.info.split("\n"))
        return s

    def last_page():
        doc = "The last_page property."
        def fget(self):
            if self.last_page_number:
                return BookPage.objects.get(page_number=self.last_page_number)
            else:
                last_page_number = BookPage.objects.filter(
                    book_number=self.book_number
                    ).aggregate(
                    last=models.Max('page_number')
                    )['last']
                return BookPage.objects.get(page_number=last_page_number)
        def fset(self, value):
            self.last_page_number = value.page_number
        def fdel(self):
            self.last_page_number = None
        return locals()
    last_page = property(**last_page())

    def get_absolute_url(self):
        return reverse('bookindex', args=[str(self.id)])

    def get_bookrank(self):
        return BookRank.objects.get_or_create(book=self)[0]

    def get_category_url(self):
        CATEGORYS = {
            "侦探推理": "a",
            "武侠修真": "b",
            "网游动漫": "c",
            "历史军事": "d",
            "都市言情": "e",
            "散文诗词": "f",
            "玄幻魔法": "g",
        }
        return reverse('category', args=[CATEGORYS.get(self.category, "g")])



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

    def update_news(self):
        """更新书籍的最后章节和最后更新时间"""
        book = self.book
        book.last_page = self
        book.save()

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

    all_push = models.IntegerField(_("总推荐"), default=0)
    mon_push = models.IntegerField(_("月推荐"), default=0)
    wek_push = models.IntegerField(_("周推荐"), default=0)

    all_fav = models.IntegerField(_("总收藏"), default=0)

    def add_point(self):
        cursor = connection.cursor()
        cursor.execute(
            "update book_bookrank "
            "set all_point=all_point+1,mon_point=mon_point+1,wek_point=wek_point+1 "
            "where id=%s;", [self.pk])

    def add_push(self):
        cursor = connection.cursor()
        cursor.execute(
            "update book_bookrank "
            "set all_push=all_push+1,mon_push=mon_push+1,wek_push=wek_push+1 "
            "where id=%s;", [self.pk])

    def add_fav(self):
        cursor = connection.cursor()
        cursor.execute(
            "update book_bookrank "
            "set all_fav=all_fav+1 "
            "where id=%s;", [self.pk])

    def sub_fav(self):
        cursor = connection.cursor()
        cursor.execute(
            "update book_bookrank "
            "set all_fav=all_fav-1 "
            "where id=%s;", [self.pk])


class KeyValueStorage(models.Model):

    """
    当值数据过大时, 保存到 long_value 字段,
    value 字段保存 long_value 的 hashlib.sha256(self.long_value).hexdigest()
    """
    key = models.CharField(_('键名'), max_length=50, db_index=True)
    value = models.CharField(_('短值'), max_length=128, blank=True)
    long_value = models.TextField(_('长值'), blank=True, default='')

    class Meta:
        verbose_name = _('KeyValueStorage')
        verbose_name_plural = _('KeyValueStorages')

    def __unicode__(self):
        return self.key

    def val():
        def fget(self):
            if not self.long_value:
                return self.value
            else:
                return pickle.loads(str(self.long_value))

        def fset(self, value):
            if isinstance(value, (str, unicode)) and len(value) < 128:
                self.value = value
                self.long_value = ""
            else:
                self.long_value = pickle.dumps(value)
                self.value = hashlib.sha256(self.long_value).hexdigest()

        def fdel(self):
            pass
        return locals()
    val = property(**val())
