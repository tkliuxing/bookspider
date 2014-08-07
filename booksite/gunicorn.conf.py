# -*- coding: utf-8 -*-
import multiprocessing

bind = "127.0.0.1:8888"
workers = multiprocessing.cpu_count() + 1
worker_class = "gevent"
worker_connections = 3000
keepalive = 1
pidfile = '/tmp/book.gunicorn.pid'
#errorlog = '/tmp/gunicorn.error.log'