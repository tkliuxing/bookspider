# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function
import hashlib
import gzip
import redis
from StringIO import StringIO
import cPickle as pickle
from django.db import models
from django.db import connection
from django.core.urlresolvers import reverse
from django.core.files.base import ContentFile
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _
from django.template.loader import render_to_string
from pyquery import PyQuery as PQ


def front_image_path(instance, filename):
    import os
    # import uuid
    # file_name = uuid.uuid4().hex
    return os.path.join(
        'bookimg/%s/' % str(instance.book_number)[-1],
        str(instance.book_number) + '.jpg'
    )


def upsert_b(book):
    if book.title and book.author:
        site_book = B.objects.filter(title=book.title, author=book.author)
        if site_book:   # update
            sb = site_book[0]
            if sb.last_update < book.last_update:
                sb.last_update = book.last_update
                sb.save()
        else:           # create
            sb = B.objects.create(
                title=book.title,
                author=book.author,
                last_update=book.last_update,
                create_time=book.create_time,
                cover_image=book.front_image
            )
            Book.objects.filter(pk=b.pk).update(site_book=sb)


class B(models.Model):
    """Site Book model"""
    title = models.CharField(max_length=100, db_index=True)
    author = models.CharField(max_length=100, blank=True, db_index=True)
    last_update = models.DateTimeField(auto_now=True, db_index=True)
    create_time = models.DateTimeField(auto_now_add=True, db_index=True)
    is_deleted = models.BooleanField(default=False)
    cover_image = models.ImageField(
        upload_to=front_image_path, max_length=200, null=True, blank=True)

    class Meta:
        unique_together = (('title', 'author'),)

    @classmethod
    def sync_excited_book(cls):
        import time
        start_time = time.time()
        for b in Book.objects.all():
            if b.title and b.author:
                # find
                site_book = B.objects.filter(title=b.title, author=b.author)
                if site_book:   # update
                    sb = site_book[0]
                    if sb.last_update < b.last_update:
                        sb.last_update = b.last_update
                        sb.save()
                else:           # create
                    sb = B.objects.create(
                        title=b.title,
                        author=b.author,
                        last_update=b.last_update,
                        create_time=b.create_time,
                        cover_image=b.front_image
                    )
                Book.objects.filter(pk=b.pk).update(site_book=sb)
            else:
                print("No title or no author!")
        end_time = time.time()
        print("Use time: {0}'s".format(end_time - start_time))


class Book(models.Model):
    """Book model"""
    origin_url = models.TextField()
    title = models.CharField(max_length=100, blank=True)
    author = models.CharField(max_length=100, blank=True)
    category = models.CharField(max_length=20, blank=True)
    info = models.TextField(blank=True)
    book_number = models.CharField(db_index=True, max_length=24)
    last_update = models.DateTimeField(auto_now=True, db_index=True)
    last_page_number = models.IntegerField(default=0, null=True, blank=True)
    create_time = models.DateTimeField(auto_now_add=True, db_index=True)
    is_deleted = models.BooleanField(default=False) 
    front_image = models.ImageField(
        upload_to=front_image_path, max_length=200, null=True, blank=True)
    site_book = models.ForeignKey(
        B, related_name='books', null=True, blank=True)
    site = models.CharField(max_length=100, default='86696',
                            null=True, blank=True, db_index=True)

    class Meta:
        verbose_name = _('书籍')
        verbose_name_plural = _('书籍')
        unique_together = [('book_number', 'site',)]
        ordering = ['book_number']

    def __str__(self):
        return unicode(self).encode("utf-8")

    def __unicode__(self):
        return u"{0} - {1} - {2}".format(self.site, self.title, self.author)

    @property
    def info_html(self):
        s = u"\n\n".join(self.info.split("\n"))
        return s

    def delete(self, *args, **kwargs):
        RC = redis.Redis()
        book_page_origin_urls = BookPage.objects.filter(
            book_number=self.book_number).values_list("origin_url", flat=True)
        RC.delete(*book_page_origin_urls)
        BookPage.objects.filter(book_number=self.book_number).delete()
        self.is_deleted = True
        self.save()
        RC.hdel('books', str(self.book_number))

    @property
    def last_page(self):
        doc = "The last_page property."
        if self.last_page_number:
            return BookPage.objects.get(page_number=self.last_page_number)
        else:
            last_page_number = BookPage.objects.filter(
                book_number=self.book_number
            ).aggregate(
                last=models.Max('page_number')
            )['last']
            return BookPage.objects.get(page_number=last_page_number)

    @last_page.setter
    def last_page_set(self, value):
        self.last_page_number = value.page_number

    @last_page.deleter
    def last_page_del(self):
        self.last_page_number = None

    def get_last_page(self):
        return BookPage.objects.filter(book_number=self.book_number, site=self.site).order_by('page_number').last()

    def get_absolute_url(self):
        return reverse('bookinfo', args=[str(self.id)])

    def get_index_url(self):
        return reverse('bookindex', args=[str(self.id)])

    def get_bookrank(self):
        return BookRank.objects.get_or_create(book=self)[0]

    def get_category_url(self):
        CATEGORYS_KV, created = KeyValueStorage.objects.get_or_create(
            key='CATEGORYS_REVERSE',
            defaults={'value': '', 'long_value': ''}
        )
        if created:
            real_categorys = Book.objects.order_by('category').distinct(
                'category').values_list('category', flat=True)
            CATEGORYS_KV.val = {x[1]: chr(x[0]) for x in zip(
                range(97, 123), real_categorys)}
            CATEGORYS_KV.save()
        return reverse('category', args=[CATEGORYS_KV.val.get(self.category, "g")])

    def bookmark_update(self):
        from booksite.usercenter.models import BookMark
        BookMark.objects.filter(book=self).update(update=True)


@receiver(post_save, sender=Book)
def book_create(sender, instance, created, *args, **kwargs):
    b = instance
    if created and b.title and b.author:
        # find B
        site_books = B.objects.filter(title=b.title, author=b.author)
        if site_books:  # update B
            sb = site_books[0]
            if sb.last_update < b.last_update:
                sb.last_update = b.last_update
                sb.save()
        else:  # create B
            sb = B.objects.create(
                title=b.title,
                author=b.author,
                last_update=b.last_update,
                create_time=b.create_time,
                cover_image=b.front_image
            )
        Book.objects.filter(pk=b.pk).update(site_book=sb)


def bookpage_path(instance, filename):
    import os
    import uuid
    file_name = uuid.uuid4().hex
    if instance.site == '86696':
        return os.path.join('book/%s/' % instance.book_number, file_name + '.html')
    else:
        return os.path.join('book/{0}/{1}/'.format(instance.site, instance.book_number), file_name + '.html')


def bookpage_path_zip(instance, filename):
    filename = bookpage_path(instance, filename)
    return filename + '.gz'


class BookPage(models.Model):
    origin_url = models.TextField()
    title = models.CharField(max_length=100, blank=True)
    # content = models.TextField(blank=True)
    content_file = models.FileField(
        upload_to=bookpage_path_zip, null=True, blank=True)
    book_number = models.CharField(db_index=True, max_length=24)
    page_number = models.CharField(db_index=True, max_length=24)
    next_number = models.CharField(db_index=True, max_length=24, null=True, blank=True)
    prev_number = models.CharField(db_index=True, max_length=24, null=True, blank=True)
    site = models.CharField(max_length=100, default='86696',
                            null=True, blank=True, db_index=True)

    class Meta:
        verbose_name = _('章节')
        verbose_name_plural = _('章节')
        unique_together = [('page_number', 'site',)]
        ordering = ['book_number', 'page_number']

    @property
    def title_html(self):
        return self.title
        book_title = self.book.title
        s = self.title.split(" ")[1:]
        title = " ".join(s)
        if title.startswith(book_title):
            title = title[len(book_title):]
        return title

    @staticmethod
    def content_html(content):
        """纯文本段落转换为html格式段落"""
        # TODO: replace_list require store to database
        replace_list = [
            ("&lt;", "<",),
            ("&gt;", ">",),
            ("大6", "大陆",),
            ("&ldqo;", "“",),
            ("&rdqo;", "”",),
        ]
        for rep in replace_list:
            if rep[0] in content:
                content = content.replace(rep[0], rep[1])
        content = content.replace('\n', '\n\n')
        return render_to_string('book/pagerender.html', {'content_html': content}).replace('\n', '')

    @staticmethod
    def content_text(content):
        """转换html段落为纯文本段落"""
        return "\n".join([PQ(p).text() for p in PQ(content).find('p')])

    def get_raw_text_content(self):
        content_html = self.get_content()
        return BookPage.content_text(content_html)

    def get_content(self):
        """获取章节压缩文件内html文本"""
        content_gzip = gzip.GzipFile('', 'rb', 9, self.content_file.file)
        content = content_gzip.read()
        content_gzip.close()
        self.content_file.file.seek(0)
        return content.decode('utf-8')

    def set_content(self, content):
        """更新（删除并新建）章节压缩文件内html"""
        self.save_content_zip_file(content, new=(not self.content_file))

    def save_content_zip_file(self, content, new=True):
        """保存章节压缩文件，new代表是否是新增章节。新增章节会新建文件，老章节会删除并新建。"""
        if new:
            content = "\n".join(
                filter(lambda x: x, BookPage.content_html(content).split("\n")))
        else:
            self.content_file.delete()
        v_file = StringIO()
        gzip_file = gzip.GzipFile('bookpage'.encode('utf-8'), 'wb', 9, v_file)
        gzip_file.write(content.encode('utf-8'))
        gzip_file.close()
        v_file.seek(0)
        content = v_file.read()
        self.content_file.save('bookpage'.encode(
            'utf-8'), ContentFile(content))
        self.content_file.close()
        v_file.close()
        return self.save()

    @property
    def book(self):
        return Book.objects.get(book_number=self.book_number, site=self.site)

    def update_news(self):
        """更新书籍的最后章节和最后更新时间"""
        try:
            book = self.book
            book.last_page = self
            book.save()
            book.bookmark_update()
        except:
            pass

    def get_absolute_url(self):
        return reverse('bookpage', kwargs={'book_id': self.book.id, 'page_number': self.page_number})

    def save(self, *args, **kwargs):
        try:
            Book.objects.get(book_number=self.book_number, site=self.site, is_deleted=False)
        except Book.DoesNotExist:
            return
        else:
            super(BookPage, self).save(*args, **kwargs)


class BookRank(models.Model):

    class Meta:
        verbose_name = _('BookRank')
        verbose_name_plural = _('BookRanks')

    book = models.OneToOneField(Book)
    site_book = models.OneToOneField(B, null=True, blank=True)

    all_point = models.IntegerField(_("总点击"), default=0)
    mon_point = models.IntegerField(_("月点击"), default=0)
    wek_point = models.IntegerField(_("周点击"), default=0)

    all_push = models.IntegerField(_("总推荐"), default=0)
    mon_push = models.IntegerField(_("月推荐"), default=0)
    wek_push = models.IntegerField(_("周推荐"), default=0)

    all_fav = models.IntegerField(_("总收藏"), default=0)

    def add_point(self):
        cursor = connection.cursor()
        cursor.execute(
            "update book_bookrank "
            "set all_point=all_point+1,mon_point=mon_point+1,wek_point=wek_point+1 "
            "where id=%s;", [self.pk])

    def add_push(self):
        cursor = connection.cursor()
        cursor.execute(
            "update book_bookrank "
            "set all_push=all_push+1,mon_push=mon_push+1,wek_push=wek_push+1 "
            "where id=%s;", [self.pk])

    def add_fav(self):
        cursor = connection.cursor()
        cursor.execute(
            "update book_bookrank "
            "set all_fav=all_fav+1 "
            "where id=%s;", [self.pk])

    def sub_fav(self):
        cursor = connection.cursor()
        cursor.execute(
            "update book_bookrank "
            "set all_fav=all_fav-1 "
            "where id=%s;", [self.pk])


class KeyValueStorage(models.Model):

    """
    当值数据过大时, 保存到 long_value 字段,
    value 字段保存 long_value 的 hashlib.sha256(self.long_value).hexdigest()
    """
    key = models.CharField(_('键名'), max_length=50, db_index=True)
    value = models.CharField(_('短值'), max_length=128, blank=True)
    long_value = models.TextField(_('长值'), blank=True, default='')

    class Meta:
        verbose_name = _('KeyValueStorage')
        verbose_name_plural = _('KeyValueStorages')

    def __unicode__(self):
        return self.key

    def val():
        def fget(self):
            if not self.long_value:
                return self.value
            else:
                return pickle.loads(str(self.long_value))

        def fset(self, value):
            if isinstance(value, (str, unicode)) and len(value) < 128:
                self.value = value
                self.long_value = ""
            else:
                self.long_value = pickle.dumps(value)
                self.value = hashlib.sha256(self.long_value).hexdigest()

        def fdel(self):
            pass
        return locals()
    val = property(**val())
