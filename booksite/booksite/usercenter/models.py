# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import AbstractUser, BaseUserManager

from booksite.book.models import Book, BookPage


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **kwars):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            email, password=password
        )
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class User(AbstractUser):
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email

User._meta.get_field('email')._unique = True
User._meta.get_field('username')._unique = False


class BookMark(models.Model):

    '''书签'''

    user = models.ForeignKey(User, verbose_name=_("用户"))
    book = models.ForeignKey(Book, verbose_name=_("书籍"))
    page = models.ForeignKey(BookPage, verbose_name=_("章节"))
    update = models.BooleanField(verbose_name=_("有更新"), default=False)
    create_time = models.DateTimeField(auto_now_add=True)

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
