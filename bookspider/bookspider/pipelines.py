# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import redis

from scrapy.exceptions import DropItem

from bookspider.items import BookinfoItem, BookpageItem, QidianRankItem

RC = redis.Redis()


class BookinfoPipeline(object):

    def __init__(self):
        self.ids_seen = set()

    def process_item(self, item, spider):
        if not isinstance(item, BookinfoItem):
            return item
        if RC.hget('books', str(item['book_number'])):
            raise DropItem("Duplicate item found: %s" % item['book_number'])
        else:
            try:
                item.save()
                RC.hset('books', str(item['book_number']), 'True')
                print str(item['book_number']).ljust(10), "-"*10, item['title']
                return item
            except:
                RC.hset('books', str(item['book_number']), 'True')
                raise DropItem("Duplicate item found: %s" % item['book_number'])


class BookpagePipeline(object):

    def __init__(self):
        self.ids_seen = set()

    def process_item(self, item, spider):
        if not isinstance(item, BookpageItem):
            return item
        if RC.get(item['origin_url']):
            raise DropItem("Duplicate item found: %s" % item['page_number'])
        else:
            try:
                item.save()
                item.instance.update_news()
                RC.set(item['origin_url'], 'True')
                print str(item['book_number']).ljust(10), "-"*10,
                print str(item['page_number']).ljust(10), "-"*10,
                print ' '.join(item['title'].split()[1:])
                return item
            except:
                RC.set(item['origin_url'], 'True')
                raise DropItem("Duplicate item found: %s" % item['page_number'])


class QidianRankPipeline(object):

    def process_item(self, item, spider):
        if not isinstance(item, QidianRankItem):
            return item
        if item.save():
            print item["time_type"],
            print unicode(item['vip_click']).ljust(10), "-"*10,
            print item['title'].encode("utf-8")
        else:
            print item["time_type"], "-"*10, "-"*10, item['title'].encode("utf-8")
        return item
