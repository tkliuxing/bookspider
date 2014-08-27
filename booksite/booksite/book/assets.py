# -*- coding: utf-8 -*-
from django_assets import Bundle, register
css = Bundle(
    'flatui/bootstrap/css/bootstrap.css',
    'flatui/bootstrap/css/prettify.css',
    'flatui/css/flat-ui.css',
    'css/main.css',
    filters='cssutils', output='assets/app.css')
register('css_all', css)

js = Bundle(
    'flatui/js/jquery-1.8.3.min.js',
    'flatui/js/bootstrap.min.js',
    'flatui/js/bootstrap-select.js',
    'flatui/js/bootstrap-switch.js',
    'flatui/js/typeahead.js',
    'js/pagination.js',
    'js/application.js',
    'js/usercenter.js',
    filters='rjsmin', output='assets/app.js')
register('js_all', js)
