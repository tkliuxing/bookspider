# -*- coding: utf-8 -*-
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from booksite.usercenter.models import BookMark, User

class BookMarkAdmin(admin.ModelAdmin):
    list_display = ('user', 'book', 'page', 'create_time',)
    list_display_links = ['user', 'book', 'page']
    search_fields = ['book__title']
admin.site.register(BookMark, BookMarkAdmin)

admin.site.register(User, UserAdmin)
