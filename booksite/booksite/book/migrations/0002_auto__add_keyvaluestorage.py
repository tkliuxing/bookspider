# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'KeyValueStorage'
        db.create_table(u'book_keyvaluestorage', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('key', self.gf('django.db.models.fields.CharField')(max_length=50, db_index=True)),
            ('value', self.gf('django.db.models.fields.CharField')(max_length=128, blank=True)),
            ('long_value', self.gf('django.db.models.fields.TextField')(default=u'', blank=True)),
        ))
        db.send_create_signal(u'book', ['KeyValueStorage'])


    def backwards(self, orm):
        # Deleting model 'KeyValueStorage'
        db.delete_table(u'book_keyvaluestorage')


    models = {
        u'book.book': {
            'Meta': {'ordering': "[u'book_number']", 'object_name': 'Book'},
            'author': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'book_number': ('django.db.models.fields.IntegerField', [], {'unique': 'True', 'db_index': 'True'}),
            'category': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'info': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'origin_url': ('django.db.models.fields.TextField', [], {}),
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