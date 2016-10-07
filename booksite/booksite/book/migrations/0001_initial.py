# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.postgres.fields
import booksite.book.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('origin_url', models.TextField()),
                ('title', models.CharField(max_length=100, blank=True)),
                ('author', models.CharField(max_length=100, blank=True)),
                ('category', models.CharField(max_length=20, blank=True)),
                ('info', models.TextField(blank=True)),
                ('book_number', models.IntegerField(unique=True, db_index=True)),
                ('last_update', models.DateTimeField(default=None, auto_now=True, null=True, db_index=True)),
                ('last_page_number', models.IntegerField(default=0, null=True, blank=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('pages', django.contrib.postgres.fields.JSONField(default=[], null=True, blank=True)),
            ],
            options={
                'ordering': ['book_number'],
                'verbose_name': '\u4e66\u7c4d',
                'verbose_name_plural': '\u4e66\u7c4d',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='BookPage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('origin_url', models.TextField()),
                ('title', models.CharField(max_length=100, blank=True)),
                ('content_file', models.FileField(null=True, upload_to=booksite.book.models.bookpage_path_zip, blank=True)),
                ('book_number', models.IntegerField(db_index=True)),
                ('page_number', models.IntegerField(unique=True, db_index=True)),
                ('next_number', models.IntegerField(default=0, null=True)),
                ('prev_number', models.IntegerField(default=0, null=True)),
            ],
            options={
                'ordering': ['book_number', 'page_number'],
                'verbose_name': '\u7ae0\u8282',
                'verbose_name_plural': '\u7ae0\u8282',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='BookRank',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('all_point', models.IntegerField(default=0, verbose_name='\u603b\u70b9\u51fb')),
                ('mon_point', models.IntegerField(default=0, verbose_name='\u6708\u70b9\u51fb')),
                ('wek_point', models.IntegerField(default=0, verbose_name='\u5468\u70b9\u51fb')),
                ('all_push', models.IntegerField(default=0, verbose_name='\u603b\u63a8\u8350')),
                ('mon_push', models.IntegerField(default=0, verbose_name='\u6708\u63a8\u8350')),
                ('wek_push', models.IntegerField(default=0, verbose_name='\u5468\u63a8\u8350')),
                ('all_fav', models.IntegerField(default=0, verbose_name='\u603b\u6536\u85cf')),
                ('book', models.OneToOneField(to='book.Book')),
            ],
            options={
                'verbose_name': 'BookRank',
                'verbose_name_plural': 'BookRanks',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='KeyValueStorage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('key', models.CharField(max_length=50, verbose_name='\u952e\u540d', db_index=True)),
                ('value', models.CharField(max_length=128, verbose_name='\u77ed\u503c', blank=True)),
                ('long_value', models.TextField(default='', verbose_name='\u957f\u503c', blank=True)),
            ],
            options={
                'verbose_name': 'KeyValueStorage',
                'verbose_name_plural': 'KeyValueStorages',
            },
            bases=(models.Model,),
        ),
    ]
