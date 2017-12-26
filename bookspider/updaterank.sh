#!/usr/bin/env bash
basepath=$(cd `dirname $0`; pwd)
cd ${basepath}; /home/book/.virtualenvs/book/bin/scrapy crawl -L ERROR qidianrank