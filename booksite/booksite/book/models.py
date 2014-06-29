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
