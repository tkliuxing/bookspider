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


class QidianRankItem(Item):
    title = Field()
    vip_click = Field()

    def save(self):
        try:
            book = Book.objects.get(title=self["title"])
        except:
            return False
        else:
            book_rank = book.get_bookrank()
            book_rank.all_push = self["vip_click"]
            book_rank.save()
            return True
