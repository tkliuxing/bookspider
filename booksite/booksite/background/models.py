# -*- coding: utf-8 -*-
import re
import hashlib
import cPickle as pickle
import time
import itertools
from booksite.book.models import KeyValueStorage


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
