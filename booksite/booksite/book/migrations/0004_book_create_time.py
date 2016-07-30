# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0003_remove_book_pages'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='create_time',
            field=models.DateTimeField(default=datetime.datetime(2016, 7, 30, 16, 19, 26, 455819, tzinfo=utc), auto_now_add=True, db_index=True),
            preserve_default=False,
        ),
    ]
