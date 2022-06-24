# Scrapy settings for boss project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'boss'

SPIDER_MODULES = ['boss.spiders']
NEWSPIDER_MODULE = 'boss.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'boss (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 0.3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="98", "Google Chrome";v="98"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-User': '?1',
    'Sec-Fetch-Dest': 'document',
    'Referer': 'https://www.zhipin.com/web/common/security-check.html?seed=XIGM%2F5eZ6zvjeSqLg63bwI4Jigp%2BPTxX00qZjiHcYobp0JiBYVDoyrJiq6U2WJkwDg9LxHXmKl10UezJW1p%2FSQ%3D%3D&name=5a4d3896&ts=1655974329430&callbackUrl=%2Fc100010000-p100101%2F%3Fpage%3D2&srcReferer=',
    'Accept-Language': 'zh-CN,zh;q=0.9',
'cookie': '_9755xjdesxxd_=32; YD00951578218230%3AWM_TID=TNUb8FbfY%2FJEBFAEAQPVQzBtaJeYRQ8%2B; _bl_uid=0ylC14kh6htf31q314w05g3w9v4F; wd_guid=1f214701-3e94-48a0-9e81-9dbfa9c99891; historyState=state; lastCity=100010000; gdxidpyhxdE=aczuO816EDmBjv79%2FEf01uuhHL8oh5E9A3Vco%2FylPm0D9WlyocD9%5CIqohT%5CeflpkSeVqKQnQyaZPBM8o0V1xQJOljTMzfzu7ggqP6bOZA3b1aYZWEGHjMUArfY0V5WzfMnPV6JDTjHgVpsiL8W4%2BPufCPv2nojY%2BI83l21yU%5C8d4thQ0%3A1654852199870; YD00951578218230%3AWM_NI=SRQ61Rsq1TT4YGA9H1QONaS4iSURVPsK4cbIdFBV7f42CpaUHXZl2nrO4mYgGBPvAt3t2NNBaXVriIZpM%2FMD5XDYz7gFRGgAtJOoIryFtvFLwaT9kcb1oxD0pGT6ZSwzcEI%3D; YD00951578218230%3AWM_NIKE=9ca17ae2e6ffcda170e2e6eeb8ce468def9daef325b6ef8ba2d45a878a8f86d85eaf8da4daeb63fceea687fc2af0fea7c3b92a918e9fd7b45ab1afffb5d7409b998fdacb3b93918282d240ab8d9bb3d55cb195fc84e143a89a8eb7b66ef8ee8d91e45f8c88968db166b291fc8edc6d859ea097c480f1acfeafcd4aa3889a93ec439ab083d0d050f7888cbaf93da59a9ea8e64bb8968190cc7abb9abc97c548b5bf9cdaea69a2efa199c73cb4999cd7d959b5a6ada6cc37e2a3; wt2=D4nEQDPdXKhI9JY__qsqgMJaE0aHFwgR20JNrTIGDrzj0tNxjjkGD2KoUVoMFNUrjCpSRwz0yu4lgOh1SYnWtwg~~; wbg=0; warlockjssdkcross=%7B%22distinct_id%22%3A%2241050099%22%2C%22first_id%22%3A%221818adf18d2c7a-0aa8356d182d38-a3e3164-1024000-1818adf18d31357%22%2C%22props%22%3A%7B%7D%2C%22device_id%22%3A%221818adf18d2c7a-0aa8356d182d38-a3e3164-1024000-1818adf18d31357%22%7D; acw_tc=0a099dd616559740305491752e0175aadd497b11e5808bad418a8132fc2a3d; __g=-; Hm_lvt_194df3105ad7148dcf2b98a91b5e727a=1654756843,1655088625,1655891539,1655974031; __l=l=%2Fwww.zhipin.com%2Fjob_detail%2F30a498935f162c011XZ709S8ElBR.html&r=&g=&s=3&friend_source=0&s=3&friend_source=0; Hm_lpvt_194df3105ad7148dcf2b98a91b5e727a=1655975189; __c=1655974030; __a=81015083.1647099806.1655891539.1655974030.329.12.14.36; __zp_stoken__=93b4dOGdoWAwBQxUtBGFHWTI8FGR8bzgaN2UIWDFhU0xGe3pdaTAndmpGBWpzHkMPfiAHIQM7NwkgNQIVfk9MPRB2JAk1W2RKbj0hWkkPBVEMRwtPGVkbf2FKUlwdeToMPBk1XwZEXXQ2dAc%3D; geek_zp_token=V1RdsnFOT901dgXdNsyhQfLCO25D_ewg~~'
}
#SPIDER_MIDDLEWARES = {
#    'boss.middlewares.BossSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
   'boss.middlewares.BossDownloaderMiddleware': 543,
   # 'boss.middlewares.RandomIPMiddleware': 400,
}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   # 'boss.pipelines.BossPipeline': 300,
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


# Redis
PROXY_REDIS_IP = '123.56.87.41'
PROXY_REDIS_PORT = 6379
PROXY_REDIS_DB = 0
PROXY_REDIS_PASSWD = '$SMe9ndaZQw$4bJ2'



MYSQL_HOST = '127.0.0.1'
MYSQL_PORT = 3306
MYSQL_USER = 'root'
MYSQL_PASSWD = '123456'
MYSQL_DB = 'stu'
MYSQL_CHARSET = 'utf8'


