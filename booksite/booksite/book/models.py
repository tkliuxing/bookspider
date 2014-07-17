# -*- coding: utf-8 -*-
from django.db import models
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

    @models.permalink
    def get_absolute_url(self):
        return ('bookindex', [str(self.id)])


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
            (u"大6",u"大陆"),
        ]
        changed = False
        for rep in replace_list:
            if rep[0] in self.content:
                self.content = self.content.replace(rep[0], rep[1])
                changed = True
        if changed:
            self.save()
        c = self.content.replace('\n','\n\n')
        return c

    @models.permalink
    def get_absolute_url(self):
        return ('bookpage', [str(self.page_number)])


class Category(models.Model):
    name = models.CharField(_('Category name'), max_length=50)

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ('')


    
