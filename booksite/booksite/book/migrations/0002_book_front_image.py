# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import booksite.book.models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='front_image',
            field=models.ImageField(max_length=200, null=True, upload_to=booksite.book.models.front_image_path, blank=True),
            preserve_default=True,
        ),
    ]
