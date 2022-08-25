# -*- coding: utf-8 -*-

# Scrapy settings for chongqing project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'chongqing'

SPIDER_MODULES = ['chongqing.spiders']
NEWSPIDER_MODULE = 'chongqing.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'chongqing (+http://www.yourdomain.com)'

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
COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
  'Accept-Language': 'en',
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.128 Safari/537.36',
'Cookie': 'zh_choose=s; zh_choose=s; xqOYlxg4MJSh80S=8.FWLqPstxrgCNlTpOK0hMHxzox0Nn4GWijKWRUwCsbYDzMahUekteufSNzlEFOK; xqOYlxg4MJShenable=true; yfx_c_g_u_id_10001434=_ck22010411310217378175871902431; yfx_f_l_v_t_10001434=f_t_1641267062733__r_t_1641267062733__v_t_1641272561365__r_c_0; xqOYlxg4MJSh80T=4Ls6JosFvNy3m97nHCmGB0ehYuj3vXnDem8_Cn0YntzvGi3DIXDdD8.o5DzVOURNAtboERA1B2EOTzxWvNPFL0kfxC154To9jFPr1C7H2LINyl_57SWH.Jl7iOsyYRqnhuO2X7QbkOkNw7.ynJBPkwF4Ydu47aQ9wG7hLHyLGCzrMdOv1mj6qyR4pSM5gjZyGxJFbPgAiiWTEUr1sipUx4iJlt00uWP93H8FFZeDFD2u4RnVmd9qBcCNOY8FuPgVBphvS0nkyR9.MLUd0L7p5Nw5yfjfvK6nOUckaOiIDeRl1bEwbFGm.kRh6E4nS3bnmV5nv5pFVWT7_OfMFguxMPKn.0k3Gcz4274qbYutXwd0EFG'
}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'chongqing.middlewares.ChongqingSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
   'chongqing.middlewares.IPProxyDownloadMiddleware': 543,
}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   'chongqing.pipelines.ChongqingPipeline': 300,
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
