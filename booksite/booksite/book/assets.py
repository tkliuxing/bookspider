# -*- coding: utf-8 -*-
from django_assets import Bundle, register
from webassets.filter import get_filter
less_filter = get_filter('less', line_numbers='comments')
css = Bundle(
    Bundle(
        'bootstrap3/less/bootstrap.less',
        filters=less_filter,
        depends='bootstrap3/less/*.less',
        output='assets/bootstrap3.css'
    ),
    Bundle(
        'botspmd/less/material.less',
        'botspmd/less/ripples.less',
        filters=less_filter,
        depends='botspmd/less/*.less',
        output='assets/material.css'
    ),
    Bundle(
        'Swiper-3.3.1/src/less/swiper.less',
        filters=less_filter,
        depends='Swiper-3.3.1/src/less/*.less',
        output='assets/swiper.css'
    ),
    Bundle(
        'css/main.less',
        filters=less_filter,
        depends='css/*.less',
        output='assets/main.css'
    ),
    filters='cssutils',
    output='assets/app.css')
register('css_all', css)

js = Bundle(
    'flatui/js/jquery-1.8.3.min.js',
    'bootstrap3/js/bootstrap.js',
    'botspmd/scripts/ripples.js',
    'botspmd/scripts/material.js',
    'Swiper-3.3.1/dist/js/swiper.jquery.js',
    'js/spin.min.js',
    'js/jquery.spin.js',
    'js/pagination.js',
    'js/application.js',
    'js/usercenter.js',
    filters='rjsmin',
    output='assets/app.js')
register('js_all', js)
