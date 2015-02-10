# -*- coding: utf-8 -*-
from django.contrib import admin
from django.forms import ModelForm, TextInput, Textarea, CharField

from booksite.book.models import Book, BookPage, KeyValueStorage


class BookForm(ModelForm):
    class Meta:
        model = Book
        widgets = {
            'origin_url': TextInput(attrs={'class':"vTextField"})
        }


class BookAdmin(admin.ModelAdmin):
    list_display = ('book_number', 'title', 'author', 'category',)
    list_display_links = ['book_number', 'title']
    search_fields = ['book_number', 'title', 'category', 'author']
    form = BookForm
admin.site.register(Book, BookAdmin)


class BookPageForm(ModelForm):
    class Meta:
        model = BookPage
        widgets = {
            'origin_url': TextInput(attrs={'class':"vTextField"})
        }


class BookPageAdmin(admin.ModelAdmin):
    list_display = ('book_number', 'title', 'page_number',)
    list_display_links = ['book_number', 'page_number', 'title']
    search_fields = ['book_number', 'page_number']
    form = BookPageForm
admin.site.register(BookPage, BookPageAdmin)


class KeyValueStorageForm(ModelForm):
    class Meta:
        model = KeyValueStorage
        fields = ('key','value','long_value',)
        widgets = {
            'key': TextInput(attrs={'disabled':"true","class":"vTextField"}),
            'value': Textarea(attrs={'disabled':"true","style":"width:500px;height:50px;"}),
            'long_value': Textarea(attrs={'disabled':"true","style":"width:500px;height:150px;"}),
        }


class KVAdmin(admin.ModelAdmin):
    list_display = ('key','val',)
    list_display_links = ['key']
    search_fields = ['key']
    form = KeyValueStorageForm
admin.site.register(KeyValueStorage, KVAdmin)
