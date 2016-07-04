# -*- coding: utf-8 -*-
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

DEBUG = True
ALLOWED_HOSTS = ['localhost', '127.0.0.1', '.kanxiaoshuo.me']
TEMPLATE_DEBUG = DEBUG

TIME_ZONE = 'Asia/Shanghai'

SECRET_KEY = 'ag0$x$$7&jjocm9pz%ob+bqx24yaa)h#-u%6=kt8#!57fre)bc'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'book',
        'USER': 'booksite',
        'PASSWORD': 'tyhbvfg56',
        'HOST': 'localhost',
    }
}

DATABASE_POOL_ARGS = {
    'max_overflow': 10,
    'pool_size': 5,
    'recycle': 300
}

CACHES = {
    'default': {
        'BACKEND': 'redis_cache.cache.RedisCache',
        'LOCATION': '127.0.0.1:6379:1',
        'KEY_PREFIX': 'booksite',
        'OPTIONS': {
            'CLIENT_CLASS': 'redis_cache.client.DefaultClient',
            'PASSWORD': '',
        }
    }
}

SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
SESSION_CACHE_ALIAS = 'default'

BROKER_URL = 'redis://localhost/2'
BAIDUTONGJI_ID = 'c6238214a1e402b8eacea64bbf3bcc61'

STATIC_ROOT = '/var/www/book/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'bookstore')
MEDIA_URL = '/media/'

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_SUBJECT_PREFIX = u'[kanxiaoshuo.me]'
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'kanxiaoshuome@gmail.com'
EMAIL_HOST_PASSWORD = 'PufsYREmR6vP'

""" Supervisor:
[program:booksite]
command=/home/book/.virtualenvs/book/bin/gunicorn booksite.wsgi
directory=/home/book/bookspider/booksite
autorestart=true
autostart=true
redirect_stderr=true
stdout_logfile=/tmp/booksite.stdout.log
"""

""" Nginx:
server {
        listen 80;

        server_name www.kanxiaoshuo.me;

        gzip on;
        gzip_static on;
        gzip_http_version 1.0;
        gzip_disable "MSIE [1-6]\.";
        gzip_vary on;
        gzip_types text/plain text/html text/css application/x-javascript text/xml application/xml application/xml+rss text/javascript;

        location / {
                proxy_pass http://127.0.0.1:8090;
                proxy_set_header Host $host;
                proxy_set_header X-Real-IP $remote_addr;
                proxy_set_header X-Forwarded-For $remote_addr;
                proxy_set_header REMOTE-HOST $remote_addr;
                proxy_redirect default;
        }
        location /static {
                alias /var/www/book;
        }
        location /media/book {
                alias /home/book/bookspider/booksite/bookstore/book;
        }
        location /media {
                alias /home/book/bookspider/booksite/bookstore;
        }
}
"""

""" Nginx Wiki:
server {
        listen 80;

        server_name wiki.oyhy.me;
        rewrite ^(.*) http://wiki.buxichu.com$1 permanent;
}
"""
