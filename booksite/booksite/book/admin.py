# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin
from django.forms import ModelForm, TextInput, Textarea

from booksite.book.models import Book, BookPage, KeyValueStorage, BookRank


class BookForm(ModelForm):
    class Meta:
        model = Book
        widgets = {
            'origin_url': TextInput(attrs={'class':"vTextField"})
        }


class BookRankInline(admin.TabularInline):
    model = BookRank


class BookDeletedListFilter(admin.SimpleListFilter):
    title = '删除状态'
    parameter_name = 'is_deleted'
    def lookups(self, request, model_admin):
        return (
            ('Yes', '已删除'),
            ('No', '未删除'),
        )
    def queryset(self, request, queryset):
        if self.value() == 'Yes':
            return queryset.filter(is_deleted__exact=True)
        if self.value() == 'No':
            return queryset.filter(is_deleted__exact=False)


class BookAdmin(admin.ModelAdmin):
    list_display = ('book_number', 'title', 'author', 'category',)
    list_display_links = ['book_number', 'title']
    list_per_page = 20
    list_max_show_all = 100
    inlines = [BookRankInline]
    search_fields = ['book_number', 'title', 'category', 'author']
    list_filter = (BookDeletedListFilter,)
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
    list_per_page = 20
    list_max_show_all = 100
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
