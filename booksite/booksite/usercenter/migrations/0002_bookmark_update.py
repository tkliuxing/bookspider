# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('usercenter', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookmark',
            name='update',
            field=models.BooleanField(default=False, verbose_name='\u6709\u66f4\u65b0'),
            preserve_default=True,
        ),
    ]
