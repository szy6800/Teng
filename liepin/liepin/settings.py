# Scrapy settings for liepin project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'liepin'

SPIDER_MODULES = ['liepin.spiders']
NEWSPIDER_MODULE = 'liepin.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'liepin (+http://www.yourdomain.com)'

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
# COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
  'Accept-Language': 'en',
'Cookie': 'gr_user_id=b21ede8f-e4bd-4638-bf5f-6a6306453010; __uuid=1654585870293.02; __gc_id=f8062ff6c43c443c86e564440b0133a4; need_bind_tel=false; new_user=false; c_flag=762cd6f483231d222d74912fdc67da8d; __s_bid=f255f61873c258e5ccc43dd6a9e8a14be406; imClientId=669dfff6133fba4e7674d3815bdeee65; imId=669dfff6133fba4e91362c0e3c63f8af; imClientId_0=669dfff6133fba4e7674d3815bdeee65; imId_0=669dfff6133fba4e91362c0e3c63f8af; gr_session_id_97dcf586237881ba=9b47339d-a101-485f-947f-41604575fc5e; __tlog=1657264799926.54%7C00000000%7C00000000%7Cs_00_pz0%7Cs_00_pz0; acw_tc=2760828516572648055505536eb14f9799da68f53ea026d4d144d9ee6e8fe8; Hm_lvt_a2647413544f5a04f00da7eee0d5e200=1657264806; fe_se=-1657264812687; UniqueKey=f8b0ac45bac241ec1a667e00ad0d9493; lt_auth=6O4JPSQMnV2q5HiKgGFfta8fjN6hAzrI9HtcgRsF1dfvWvWw4PjrQwqFr7YCxAMhx0xycMULN7X5N%2B76wXBL60IawGmklICxv%2F2k2XgeTuZnHuyflMXuqsjQQ5wtrXg6ykpgn2si; access_system=C; user_roles=0; user_photo=5f8fa3a6f6d1ab58476f322808u.png; user_name=%E7%9F%B3%E5%BC%A0%E6%AF%85; inited_user=83fc4fabea08a638acf3441819698d09; imApp_0=1; fe_im_connectJson_0=%7B%220_f8b0ac45bac241ec1a667e00ad0d9493%22%3A%7B%22socketConnect%22%3A%221%22%2C%22connectDomain%22%3A%22liepin.com%22%7D%7D; __session_seq=26; __uv_seq=26; Hm_lpvt_a2647413544f5a04f00da7eee0d5e200=1657265485; fe_im_socketSequence_new_0=23_19_4; fe_im_opened_pages=_1657264861483_1657264930578_1657264988767_1657265485466',
}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'liepin.middlewares.LiepinSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
   'liepin.middlewares.RandomUserAgentMiddleware': 543,
}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
#ITEM_PIPELINES = {
#    'liepin.pipelines.LiepinPipeline': 300,
#}

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


MYSQL_HOST = '123.126.87.123'
MYSQL_PORT = 3306
MYSQL_USER = 'root'
MYSQL_PASSWD = 'Lxp.138927!asd'
MYSQL_DB = 'crawler2022'
MYSQL_CHARSET = 'utf8'



PROXY_REDIS_IP = '123.56.87.41'
PROXY_REDIS_PORT = 6379
PROXY_REDIS_DB = 0
PROXY_REDIS_PASSWD = '$SMe9ndaZQw$4bJ2'