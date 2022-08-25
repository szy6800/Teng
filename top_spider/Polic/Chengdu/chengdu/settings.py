# -*- coding: utf-8 -*-

# Scrapy settings for chengdu project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'chengdu'

SPIDER_MODULES = ['chengdu.spiders']
NEWSPIDER_MODULE = 'chengdu.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'chengdu (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
# DOWNLOAD_DELAY = 0.2
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

'Cookie': 'yfx_c_g_u_id_10000063=_ck21120614152912277501450385725; azSsQE5NvspcS=58pETn89RDtitvj96qd_tZMw.458sMCnHaXjvLY2_02fkIeZbFANT0uYsssU24ByWfkjozLTqJxNQpm_xqFnNyA; yfx_f_l_v_t_10000063=f_t_1638771329217__r_t_1641281309885__v_t_1641281309885__r_c_1; azSsQE5NvspcT=53wHCXboseS0qqqm5EdB1YqWY5hXKliXkqGlnMGWhqlg_Z0uk90RRH3Yq5.cfgtHXQSkFwyP0_L9qbYd01yikSub1h_gkfwjwsUrLp.FZeyIyht02vSZ6Nb77i2Aw0CFr9PoOcDQHr5xRe2GskzPekl_v5dgWw3tLpbncPcG7SdgxpX_LZfj50D2FuGOhow6IUBtv.3pg_i5gncnuqiFaiYtjj7ly.WTJGLBqwugCZVQAF2yQshr5eEzX9CE5NAhk_35F8YuzF.9aohKAvu1Lk1tkJPNDM5BB4vlHG2xF.FFGxGaECkBK7vMpcEr3qwperlx4Q5VdApFNoT.9oHO0X0'
}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'chengdu.middlewares.ChengduSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
   'chengdu.middlewares.IPProxyDownloadMiddleware': 543,
}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'chengdu.pipelines.ChengduPipeline': 300,
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

