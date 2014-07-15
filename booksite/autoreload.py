#!/usr/bin/env python

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "booksite.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

from livereload import Server

server = Server(application)
server.watch('booksite/book/static')
server.watch('booksite/book/*.py')
server.watch('booksite/*.py')
server.watch('booksite/book/templates')
server.serve(port=35729)