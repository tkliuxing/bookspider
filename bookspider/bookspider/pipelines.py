# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os
import redis

from scrapy.exceptions import DropItem
from scrapy.conf import settings

from django.core.files.base import File

from bookspider.items import BookinfoItem, BookpageItem, QidianRankItem, BookPage, Book

from booksite.book.models import front_image_path

RC = redis.Redis()


class BookinfoPipeline(object):

    def __init__(self):
        self.ids_seen = set()

    def process_item(self, item, spider):
        if not isinstance(item, BookinfoItem):
            return item
        if RC.hget('books', str(item['book_number'])) and RC.hget('bookimgs', str(item['book_number'])):
            print "Duplicate item found: ", str(item['book_number']).ljust(10), "-" * 10, item['title']
            raise DropItem("Duplicate item found: %s" % item['book_number'])
        else:
            has_book = False
            # 尝试保存，失败则是有重复的
            try:
                book_obj = item.save()
            except:
                has_book = True
            if has_book:
                book_obj = Book.objects.get(book_number=item['book_number'])
            # 若有图片则丢弃
            if book_obj.front_image:
                RC.hset('bookimgs', str(item['book_number']), 'True')
                RC.hset('books', str(item['book_number']), 'True')
                raise DropItem("Duplicate item found: %s" % item['book_number'])
            print str(item['book_number']).ljust(10), "-" * 10, item['title']
            if len(item['images']) == 1:
                old_path = os.path.join(settings.get("IMAGES_STORE"), item['images'][0]['path'])
                with open(old_path, 'rb') as f:
                    book_obj.front_image.save(os.path.split(old_path)[1], File(f))
                book_obj.save()
                os.remove(old_path)
            RC.hset('bookimgs', str(item['book_number']), 'True')
            RC.hset('books', str(item['book_number']), 'True')
            return item


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
            except:
                import traceback
                traceback.print_exc()
                # RC.set(item['origin_url'], 'True')
                raise DropItem("Item save error: %s" % item['page_number'])
            try:
                item.instance.save_content_zip_file(item['content'])
                item.instance.update_news()
                RC.set(item['origin_url'], 'True')
                print str(item['book_number']).ljust(10), "-" * 10,
                print str(item['page_number']).ljust(10), "-" * 10,
                for i in item['title'].encode("utf-8").split()[1:]:
                    print i,
                print ''
                return item
            except:
                item.instance.delete()
                import traceback
                traceback.print_exc()
                # RC.set(item['origin_url'], 'True')
                raise DropItem("Item save error: %s" % item['page_number'])


class QidianRankPipeline(object):

    def process_item(self, item, spider):
        if not isinstance(item, QidianRankItem):
            return item
        if item.save():
            print item["time_type"],
            print unicode(item['vip_click']).ljust(10), "-" * 10,
            print item['title'].encode("utf-8")
        else:
            print item["time_type"], "-" * 10, "-" * 10, item['title'].encode("utf-8")
        return item
