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

sys.path.append(os.path.dirname(booksite.__file__))

os.environ['DJANGO_SETTINGS_MODULE'] = 'booksite.settings'

BOT_NAME = 'bookspider'

SPIDER_MODULES = ['bookspider.spiders']
NEWSPIDER_MODULE = 'bookspider.spiders'

REDIRECT_ENABLED = False

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'bookspider (+http://www.yourdomain.com)'

ITEM_PIPELINES = {
    'bookspider.pipelines.BookinfoPipeline': 300,
    'bookspider.pipelines.BookpagePipeline': 300,
}
