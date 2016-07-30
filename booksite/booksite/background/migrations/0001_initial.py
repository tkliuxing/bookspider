# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='NewBookLog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('book_title', models.CharField(max_length=30, verbose_name=b'Book Title')),
                ('task_id', models.CharField(max_length=36, verbose_name=b'Task UID')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
