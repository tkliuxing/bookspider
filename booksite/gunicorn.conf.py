# -*- coding: utf-8 -*-
# import multiprocessing

bind = "127.0.0.1:8888"
workers = 2
worker_class = "gevent"
worker_connections = 3000
keepalive = 1
pidfile = '/tmp/book.gunicorn.pid'
#errorlog = '/tmp/gunicorn.error.log'

try:
    from local_gunicorn import *
except ImportError:
    raise ImportError('应当添加与gunicorn.conf.py同级别目录下的local_gunicorn.py文件')
