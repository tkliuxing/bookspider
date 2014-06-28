# -*- coding: utf-8 -*-

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

DEBUG = True

TEMPLATE_DEBUG = DEBUG

SECRET_KEY = 'kr71xy)rfb=(tp!dj^e18vzc$2n-4k8rc$g!lx&4^+og%40904'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'bookspider',
        'USER': 'spider',
        'PASSWORD': 'admin',
        'HOST': '127.0.0.1',
    }
}
