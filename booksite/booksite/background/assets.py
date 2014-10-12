# -*- coding: utf-8 -*-
from django_assets import Bundle, register
css = Bundle(
    'botspmd/css/material.css',
    'botspmd/css/ripples.css',
    'css/background.css',
    filters='cssutils', output='assets/bkg_app.css')
register('css_all_bkg', css)

js = Bundle(
    'bootstrap3/js/bootstrap.js',
    'botspmd/scripts/ripples.js',
    'botspmd/scripts/material.js',
    'js/pagination.js',
    'js/background.js',
    filters='rjsmin', output='assets/bkg_app.js')
register('js_all_bkg', js)
