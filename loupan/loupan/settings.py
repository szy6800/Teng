# Scrapy settings for loupan project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'loupan'

SPIDER_MODULES = ['loupan.spiders']
NEWSPIDER_MODULE = 'loupan.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'loupan (+http://www.yourdomain.com)'

# robot协议,超时,警告等级
ROBOTSTXT_OBEY = False
DOWNLOAD_TIMEOUT = 16
# LOG_LEVEL = 'INFO'

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 0.4
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

"cookie":"global_cookie=zh70wkfvs63wvipbgt5286ivd1zl11qybub; lastscanpage=0; city=www; resourceDetail=1; global_wapandm_cookie=osodt8ra6rq4bxhljv90pxdu51kl139970r; csrfToken=Jcouoe9x0_J6mJuz7RuPbyLb; __utma=147393320.102166071.1647929978.1648045221.1648092481.12; __utmc=147393320; __utmz=147393320.1648092481.12.5.utmcsr=search.fang.com|utmccn=(referral)|utmcmd=referral|utmcct=/; __utmt_t0=1; __utmt_t1=1; __utmt_t2=1; __utmt_t3=1; __utmt_t4=1; g_sourcepage=esf_xq%5Elb_pc; __utmb=147393320.57.10.1648092481; unique_cookie=U_xo9lq3ex2ie6iw8xuxl0jogi11sl14fp5dz*9",
"referer":"https://xian.esf.fang.com/housing/__0_3_0_0_2_0_0_0/",
"user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36",
}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'loupan.middlewares.LoupanSpiderMiddleware': 543,
#}
# U-A请求头
DOWNLOADER_MIDDLEWARES = {
   # 'loupan.middlewares.RandomUserAgentMiddleware': 543,
   # 'loupan.middlewares.RandomIPMiddleware': 543,
}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'loupan.middlewares.LoupanDownloaderMiddleware': 543,
#}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   # 'loupan.pipelines.LoupanPipeline': 300,
}
REDIRECT_ENABLED = False
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
MYSQL_HOST = '127.0.0.1'
MYSQL_PORT = 3306
MYSQL_USER = 'root'
MYSQL_PASSWD = '123456'
MYSQL_DB = 'ceshi'
MYSQL_CHARSET = 'utf8'