# Book Spider #

## 概况 ##

1. 包含一个Scrapy爬虫项目
2. 包含一个Django站点, 用来显示书籍
3. 爬虫与站点的数据模型相关联
4. 爬虫实现了以下站点的内容收集:

| 网站域名          | 爬虫名称 |
|-------------------|----------|
| www.86696.cc      | douluo   |

5. 未完成事项:
> * 站点显示
> * 书目整理
> * 评论系统
> * 投票系统
> * 书籍更新内容获取方式

## 安装使用 ##

1. 安装Python 2.7
1. 安装Pip
1. 使用pip安装Scrapy Django
1. clone本项目
1. `cd booksite && python setup.py develop`
1. 配置Django项目的 `local_settings.py` 文件,位于:`PROJECT_DIR/booksite/booksite`,配置数据库, 如:
1. 
```
	DATABASES = {
		'default': {
			'ENGINE': 'django.db.backends.mysql',
			'NAME': 'bookspider',
			'USER': 'spider',
			'PASSWORD': 'admin',
			'HOST': '127.0.0.1',
		}
	}
```
1. 生成数据库 `python manage.py syncdb`
1. 进入目录 `PROJECT_DIR/bookspider`
1. 使用Scrapy进行抓取, `scrapy crawl "爬虫名称"`