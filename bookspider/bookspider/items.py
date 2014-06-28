# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field
from scrapy.contrib.djangoitem import DjangoItem

from booksite.book.models import Book, BookPage

class BookinfoItem(DjangoItem):
    django_model = Book


class BookpageItem(DjangoItem):
    django_model = BookPage
