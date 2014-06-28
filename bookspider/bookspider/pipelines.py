# -*- coding: utf-8 -*-
import json

from scrapy.exceptions import DropItem

from bookspider.items import BookinfoItem, BookpageItem, Book, BookPage

class BookinfoPipeline(object):
    def __init__(self):
        self.ids_seen = set()
    def process_item(self, item, spider):
        if not isinstance(item, BookinfoItem):
            return item
        if item['book_number'] in self.ids_seen:
            raise DropItem("Duplicate item found: %s" % item['book_number'])
        else:
            self.ids_seen.add(item['book_number'])
            try:
                item.save()
                print str(item['book_number']).ljust(10),"-"*10,item['title']
                return item
            except:
                raise DropItem("Duplicate item found: %s" % item['book_number'])


class BookpagePipeline(object):
    def __init__(self):
        self.ids_seen = set()
    def process_item(self, item, spider):
        if not isinstance(item, BookpageItem):
            return item
        if item['page_number'] in self.ids_seen:
            raise DropItem("Duplicate item found: %s" % item['page_number'])
        else:
            self.ids_seen.add(item['page_number'])
            try:
                item.save()
                print str(item['book_number']).ljust(10),"-"*10,
                print str(item['page_number']).ljust(10),"-"*10,
                print ' '.join(item['title'].split()[1:])
                return item
            except:
                raise DropItem("Duplicate item found: %s" % item['page_number'])

