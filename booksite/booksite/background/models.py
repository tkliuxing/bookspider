# -*- coding: utf-8 -*-
import hashlib
import cPickle as pickle
import time
import itertools
from booksite.book.models import KeyValueStorage


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
        return u"%r -> %r" % (self.rule_res, self.replace_to)

    def get_hash(self):
        pickle_data = pickle.dumps([self.rule_res, self.replace_to])
        return hashlib.sha256(pickle_data).hexdigest()

    @classmethod
    def all(cls):
        def make_rule(db_obj):
            rule = cls(db_obj.val["rule_res"], db_obj.val["replace_to"])
            rule.db_data = db_obj
            rule.hash = db_obj.value
            return rule
        all_rule_data = KeyValueStorage.objects.filter(key__startswith=cls.KEY_PREFIX)
        iter_data = itertools.imap(
            make_rule,
            all_rule_data
        )
        return iter_data

    def save(self):
        self.db_data.val = {
            "rule_res": self.rule_res,
            "replace_to": self.replace_to
        }
        self.db_data.save()

    def delete(self):
        if self.db_data.pk:
            self.db_data.delete()
