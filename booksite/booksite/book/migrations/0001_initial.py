# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Book'
        db.create_table(u'book_book', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('origin_url', self.gf('django.db.models.fields.TextField')()),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('author', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('category', self.gf('django.db.models.fields.CharField')(max_length=20, blank=True)),
            ('info', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('book_number', self.gf('django.db.models.fields.IntegerField')(unique=True, db_index=True)),
        ))
        db.send_create_signal(u'book', ['Book'])

        # Adding model 'BookPage'
        db.create_table(u'book_bookpage', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('origin_url', self.gf('django.db.models.fields.TextField')()),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('content', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('book_number', self.gf('django.db.models.fields.IntegerField')(db_index=True)),
            ('page_number', self.gf('django.db.models.fields.IntegerField')(unique=True, db_index=True)),
            ('next_number', self.gf('django.db.models.fields.IntegerField')(default=0, null=True)),
            ('prev_number', self.gf('django.db.models.fields.IntegerField')(default=0, null=True)),
        ))
        db.send_create_signal(u'book', ['BookPage'])

        # Adding model 'BookRank'
        db.create_table(u'book_bookrank', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('book', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['book.Book'], unique=True)),
            ('all_point', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('mon_point', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('wek_point', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('all_push', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('mon_push', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('wek_push', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('all_fav', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal(u'book', ['BookRank'])


    def backwards(self, orm):
        # Deleting model 'Book'
        db.delete_table(u'book_book')

        # Deleting model 'BookPage'
        db.delete_table(u'book_bookpage')

        # Deleting model 'BookRank'
        db.delete_table(u'book_bookrank')


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
        }
    }

    complete_apps = ['book']