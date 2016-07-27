# -*- coding: utf-8 -*-
from __future__ import absolute_import

import os
import raven

from celery import Celery
from raven.contrib.celery import register_signal, register_logger_signal
from django.conf import settings

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'booksite.settings')

class MyCelery(Celery):

    def on_configure(self):
        sentry_dsn = getattr(settings, 'SENTRY_DSN', None)
        if sentry_dsn is None:
            return super(MyCelery, self).on_configure()
        client = raven.Client(sentry_dsn)

        # register a custom filter to filter out duplicate logs
        register_logger_signal(client)

        # hook into the Celery error handler
        register_signal(client)

app = Celery('booksite')
app.config_from_object('django.conf:settings')


# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
