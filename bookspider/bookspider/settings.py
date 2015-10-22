# -*- coding: utf-8 -*-
# Scrapy settings for bookspider project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

import os
import sys
import booksite
from django.core.wsgi import get_wsgi_application
# reload(sys)
# sys.setdefaultencoding('utf-8')
sys.path.append(os.path.dirname(booksite.__file__))

os.environ['DJANGO_SETTINGS_MODULE'] = 'booksite.settings'
from django.conf import settings as djsettings

application = get_wsgi_application()

BOT_NAME = 'bookspider'

SPIDER_MODULES = ['bookspider.spiders']
NEWSPIDER_MODULE = 'bookspider.spiders'

REDIRECT_ENABLED = False

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'bookspider (+http://www.yourdomain.com)'

IMAGES_STORE = os.path.join(djsettings.MEDIA_ROOT, 'bookimgs')

ITEM_PIPELINES = {
    'scrapy.pipelines.images.ImagesPipeline': 1,
    'bookspider.pipelines.BookinfoPipeline': 300,
    'bookspider.pipelines.BookpagePipeline': 300,
    'bookspider.pipelines.QidianRankPipeline': 300,
}

DOWNLOADER_MIDDLEWARES = {
    'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 110,
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
    'bookspider.middlewares.ProxyMiddleware': 100,
    'bookspider.middlewares.RotateUserAgentMiddleware': 400
}

PROXY_LIST = [
    "111.13.55.3:22",
    "114.112.91.97:90",
    "117.135.194.53:80",
    "117.135.250.53:80",
    "117.135.250.56:80",
    "117.135.252.14:80",
    "120.198.243.14:80",
    "120.198.243.15:80",
    "122.225.106.36:80",
    "122.225.106.40:80",
    "122.96.59.106:80",
    "182.118.23.7:8081",
    "183.136.135.153:8080",
    "183.207.224.12:80",
    "183.207.224.44:80",
    "183.207.224.45:80",
    "183.207.228.119:80",
    "183.207.228.51:80",
    "183.207.228.8:80",
    "183.207.228.9:89",
    "202.108.23.247:80",
    "218.206.83.89:80",
    "220.181.32.106:80",
    "221.10.102.199:82",
    "221.10.102.203:82",
    "222.161.248.122:80",
    "222.161.248.124:80",
    "27.202.7.247:80",
    "60.206.153.177:8118",
    "61.184.192.42:80",
]

try:
    from .local_settings import *
except:
    raise ImportError('应当使用与settings同级别目录下的local_settings文件')
