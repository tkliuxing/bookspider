# -*- coding: utf-8 -*-
import re
import hashlib
import cPickle as pickle
import time
import itertools
import uuid
from django.db import models
from booksite.book.models import KeyValueStorage, Book


class GetRuleError(Exception):
    pass


class ReplaceRule(object):
    KEY_PREFIX = "replace_rule_"

    def __init__(self, rule_res, replace_to):
        self.rule_res = rule_res
        self.replace_to = replace_to
        self.hash = self.get_hash()
        self.db_data = KeyValueStorage()
        self.db_data.key = ReplaceRule.KEY_PREFIX + str(int(time.time()))
        self.db_data.val = {
            "rule_res": self.rule_res,
            "replace_to": self.replace_to
        }

    def __str__(self):
        return unicode(self).encode("utf-8")

    def __unicode__(self):
        try:
            return u"'%s' -> '%s'" % (
                self.rule_res.decode("utf-8"),
                self.replace_to.decode("utf-8"),
            )
        except:
            return u"'%s' -> '%s'" % (
                self.rule_res,
                self.replace_to,
            )

    def get_hash(self):
        pickle_data = pickle.dumps([self.rule_res, self.replace_to])
        return hashlib.sha256(pickle_data).hexdigest()

    def replace(self, content, flags=0):
        rex = re.compile(self.rule_res, flags)
        return rex.sub(self.replace_to, content)

    def findall(self, content, flags=0):
        rex = re.compile(self.rule_res, flags)
        return rex.findall(content)

    def match(self, content, flags=0):
        rex = re.compile(self.rule_res, flags)
        return rex.search(content)

    @classmethod
    def make_rule(cls, db_obj):
        rule = cls(db_obj.val["rule_res"], db_obj.val["replace_to"])
        rule.db_data = db_obj
        rule.hash = db_obj.value
        return rule

    @classmethod
    def all(cls):
        all_rule_data = KeyValueStorage.objects.filter(key__startswith=cls.KEY_PREFIX).order_by("-key")
        iter_data = itertools.imap(
            cls.make_rule,
            all_rule_data
        )
        return iter_data

    @classmethod
    def get(cls, pk=0):
        if not pk:
            raise GetRuleError("primary key error! primary key[%s]" % pk)
        try:
            db_data = KeyValueStorage.objects.get(pk=pk)
        except KeyValueStorage.DoesNotExist:
            raise GetRuleError("DoesNotExist! primary key[%s]" % pk)
        else:
            return cls.make_rule(db_data)

    def save(self):
        self.db_data.val = {
            "rule_res": self.rule_res,
            "replace_to": self.replace_to
        }
        self.db_data.save()

    def delete(self):
        if self.db_data.pk:
            self.db_data.delete()


class ImplementError(BaseException):
    pass


class TuiJianObj(object):

    def __init__(self):
        if not hasattr(self, 'KEY'):
            raise ImplementError('TuiJianObj need inherit.')
        ft_data, created = KeyValueStorage.objects.get_or_create(key=self.KEY)
        if created:
            self.book_id_list = []
        else:
            self.book_id_list = ft_data.val or []
        self.books = self._build_books()

    def _build_books(self):
        books = []
        for book_id in self.book_id_list:
            try:
                books.append(Book.objects.get(id=book_id))
            except Book.DoesNotExist:
                pass
        return books

    def __str__(self):
        return unicode(self).encode("utf-8")

    def __unicode__(self):
        return "|".join(self.books.objects.values_list("title", flat=True))

    def add(self, book):
        self.book_id_list.append(book.id)
        self.books.append(book)

    def remove(self, book):
        if book.id in self.book_id_list:
            self.book_id_list.remove(book.id)
            self.books = self._build_books()

    def save(self):
        data = KeyValueStorage.objects.get_or_create(key=self.KEY)[0]
        data.val = self.book_id_list
        data.save()


class FengTui(TuiJianObj):
    KEY = "fengtui"


class JingTui(TuiJianObj):
    KEY = "jingtui"

class NewBookLog(models.Model):
    """获取新书的记录信息"""
    create_time = models.DateTimeField(auto_now_add=True)
    book_title = models.CharField('Book Title', max_length=30)
    task_id = models.CharField('Task UID', max_length=36)

    def get_task_uuid(self):
        if self.task_id:
            try:
                return uuid.UUID(str(self.task_id))
            except ValueError as e:
                return None
        return None