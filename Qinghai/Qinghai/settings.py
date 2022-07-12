# -*- coding: utf-8 -*-

# Scrapy settings for Qinghai project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'Qinghai'

SPIDER_MODULES = ['Qinghai.spiders']
NEWSPIDER_MODULE = 'Qinghai.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'Qinghai (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 0.2
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
# COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
  'Accept-Language': 'en',
}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'Qinghai.middlewares.QinghaiSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
   'Qinghai.middlewares.RandomUserAgentMiddleware': 143,
   # 'Qinghai.middlewares.RandomIPMiddleware': 40,

}


# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}


# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   'Qinghai.pipelines.QinghaiPipeline': 300,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'


# # 测试
# MYSQL_HOST = '127.0.0.1'
# MYSQL_PORT = 3306
# MYSQL_USER = 'root'
# MYSQL_PASSWD = '123456'
# MYSQL_DB = 'ceshi'
# MYSQL_CHARSET = 'utf8'

# # 阿里云mysql
# MYSQL_HOST = '123.56.87.41'
# MYSQL_PORT = 3306
# MYSQL_USER = 'root'
# MYSQL_PASSWD = 'I0z>kp9tnavw'
# MYSQL_DB = 'crawler2021'
# MYSQL_CHARSET = 'utf8'


MYSQL_HOST = '123.126.87.125'
MYSQL_PORT = 3307
MYSQL_USER = 'root'
MYSQL_PASSWD = 'Zfw3aVMkb^KVew6q'
MYSQL_DB = 'crawler2021'
MYSQL_CHARSET = 'utf8'

# MYSQL_HOST = '123.126.87.123'
# MYSQL_PORT = 3306
# MYSQL_USER = 'root'
# MYSQL_PASSWD = 'Lxp.138927!asd'
# MYSQL_DB = 'crawler2022'
# MYSQL_CHARSET = 'utf8'



PROXY_REDIS_IP = '123.56.87.41'
PROXY_REDIS_PORT = 6379
PROXY_REDIS_DB = 0
PROXY_REDIS_PASSWD = '$SMe9ndaZQw$4bJ2'
