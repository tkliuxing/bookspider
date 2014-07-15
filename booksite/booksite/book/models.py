# -*- coding: utf-8 -*-
from django.db import models

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
        from django.core.urlresolvers import reverse
        return reverse('bookindex', kwargs={'book_id':str(self.id)})


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
        if u"大6" in self.content:
            converts = self.content.replace(u"大6",u"大陆")
            self.content = converts
            self.save()
        c = self.content.replace('\n','\n\n')
        return c

    def get_absolute_url(self):
        from django.core.urlresolvers import reverse
        return reverse('bookpage', kwargs={'page_number':str(self.page_number)})
