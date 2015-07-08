# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Book.pages'
        db.add_column(u'book_book', 'pages',
                      self.gf('django_pgjson.fields.JsonBField')(default=[]),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Book.pages'
        db.delete_column(u'book_book', 'pages')


    models = {
        u'book.book': {
            'Meta': {'ordering': "[u'book_number']", 'object_name': 'Book'},
            'author': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'book_number': ('django.db.models.fields.IntegerField', [], {'unique': 'True', 'db_index': 'True'}),
            'category': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'info': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'is_deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_page_number': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'last_update': ('django.db.models.fields.DateTimeField', [], {'default': 'None', 'auto_now': 'True', 'null': 'True', 'db_index': 'True', 'blank': 'True'}),
            'origin_url': ('django.db.models.fields.TextField', [], {}),
            'pages': ('django_pgjson.fields.JsonBField', [], {'default': '[]'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'})
        },
        u'book.bookpage': {
            'Meta': {'ordering': "[u'book_number', u'page_number']", 'object_name': 'BookPage'},
            'book_number': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'}),
            'content': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'next_number': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True'}),
            'origin_url': ('django.db.models.fields.TextField', [], {}),
            'page_number': ('django.db.models.fields.IntegerField', [], {'unique': 'True', 'db_index': 'True'}),
            'prev_number': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'})
        },
        u'book.bookrank': {
            'Meta': {'object_name': 'BookRank'},
            'all_fav': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'all_point': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'all_push': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'book': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['book.Book']", 'unique': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mon_point': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'mon_push': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'wek_point': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'wek_push': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        u'book.keyvaluestorage': {
            'Meta': {'object_name': 'KeyValueStorage'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '50', 'db_index': 'True'}),
            'long_value': ('django.db.models.fields.TextField', [], {'default': "u''", 'blank': 'True'}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '128', 'blank': 'True'})
        }
    }

    complete_apps = ['book']