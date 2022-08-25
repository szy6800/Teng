# -*- coding: utf-8 -*-

# Scrapy settings for shenyang project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'shenyang'

SPIDER_MODULES = ['shenyang.spiders']
NEWSPIDER_MODULE = 'shenyang.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'shenyang (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
    # "content-type": "application/json; charset=UTF-8",
    # "cookie": "__apex_test__=; __apex_test__=; .AspNetCore.Antiforgery.ZBV4UtDBfxE=CfDJ8AK6OlKaHqBOv-0HfQbSCntgaz9VjbksVEctCBuNdeQsPkSHHepqlwlQFuMxzLVKIizEc60nbFC2e50hdbWkKSHlk4ix0MwkyhbP2Cy5OfQY51kNNTCLN79tqZtnYW4p65IYP-X3L0AXbMG-rto0fwY; __utmc=58757803; __utmz=58757803.1621560862.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); intercom-id-h8gelaf5=8fe676a1-2191-4a5f-a1ea-d5801c0a65a1; __stripe_mid=b2be280b-2ad9-4d98-9eb7-9383571fe14efab308; _upscope__region=ImFwLXNvdXRoZWFzdCI=; _upscope__everConnected=dHJ1ZQ==; __utma=58757803.1992929374.1621560862.1621560862.1621583345.2; __apex_test__=; _upscope__shortId=IllRRlhMRkJKVDMzSk1YWU5EIg==; WDBUT.v2=Q2ZESjhBSzZPbEthSHFCT3YtMEhmUWJTQ25zZTduZzJYSURueDUtSUVwbllRejRXb3FaNDA3bW9KQmhGUzlSeUl5T1cwbldjYi03ZGtTTWxST3pVNEgyOUpyNmVkTEZqWkhiVmJOWTdsZUlQX1R4NkhLc2h0Skc4X0pJYXdKMjlOZ0lQZXloQXQ3cFp1Y2tsb1RVckxzN3RaSFZLa2t1RkpMTXhvQ0Y4aDNGam5BWU9QbC1IYmlwVjd0RC1sWFBoczdaSWtSRjNFbGRERE94U3hNSTdZYVp5UFFJaWM4NDd3VjZham9FbWpqVXgybjJvN1laSkJnV2JCeTh1Zkc3bFVNR2s1MnMwUWMtbm5KVU0yTEhYeU1zQktBcw%3D%3D; intercom-session-h8gelaf5=U2FObEluM2xyTTM5cytJSjEvRnpSejVDUlc4bVAxanFDY24rWHJTNFQxdWIwOXMxRlRiWDl5QTRaaGEySjRuQi0tTUxuN3dTdngvTjZrZzZsR0VoaDR1UT09--607faf364775e53b37a5f8f07880cb3dc5af682f; wdb.App.v2=CfDJ8AK6OlKaHqBOv-0HfQbSCnuvX8WgqKGRm3CWcpoNaPPVkJS1AEiVseAi93wiegXYFAmr6KDyex4OpDoQGpOPvTN8wHqe-WRR_oxdo2gnlUCi-PT5rJ2JMxMCyM-qTOZODa7-WMa6B6s2kj6kzgC-k_NxMlQcYl1yMV5KRr-3J75lpDku0VKyhjqiAyXVqftcUpZYFNbakXRJ3pAeLAxAxBz1h93sP4XOfeygGkgI7BIJ4sEWXjSFv9lp84kXQ8-_uiQTsLxYKqgR9-WrbGypTmUqV4ciKgR44MoqQOqLdTUBhhNe41T9M1QdXt0feFCMSw6yl53SPvmDq5eo6Er5LZI",
    # "origin": "https://app.welldatabase.com",
    # "referer": "https://app.welldatabase.com/browse/Wells",
    # "requestverificationtoken": "CfDJ8AK6OlKaHqBOv-0HfQbSCnstVilHmnk_PEk4vy0FnGJRzSb-9NcwjCMD9rPpuhJCd1R7Pz0VB7scKjEybQXMr-D_OnEzjGZC-neF9D4LzWmAVRLiDA6X3HFmTJClmvw96QoPb6KG31PlLLh661KXEZ8bQHPF8427WNO48FEq3iAi3dWYfQi2nwYswtAf-AdRjQ",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36",
    # "x-requested-with": "XMLHttpRequest",

}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'shenyang.middlewares.ShenyangSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
   'shenyang.middlewares.ShenyangDownloaderMiddleware': 543,
}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   'shenyang.pipelines.ShenyangPipeline': 300,
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
