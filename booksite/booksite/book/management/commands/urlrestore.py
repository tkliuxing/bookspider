# -*- coding: utf-8 -*-
import redis

from django.core.management.base import BaseCommand

from booksite.book.models import BookPage

class Command(BaseCommand):
    args = ''
    help = 'Restore DB\'s BookPage url to Redis server.'

    def handle(self, *args, **options):
        RC = redis.Redis()
        urls = BookPage.objects.values_list('origin_url', flat=True)
        total = BookPage.objects.all().count()
        count = 0
        tmp_100 = 0
        tmp_1000 = 0
        self.stdout.write('loading data.\n', ending='')
        urls = list(urls)
        self.stdout.write('progress:   0% ', ending='')
        self.stdout.flush()
        for url in urls:
            RC.setnx(url, 'True')
            count += 1
            if int(float(count) / float(total) * 1000) == (tmp_1000 + 1):
                self.stdout.write('.', ending='')
                self.stdout.flush()
                tmp_1000 += 1
            if int(float(count) / float(total) * 100) == (tmp_100 + 1):
                self.stdout.write('\nprogress: %3d%% ' % (tmp_100+1,), ending='')
                self.stdout.flush()
                tmp_100 += 1
        self.stdout.write('\nAll url restored!')
