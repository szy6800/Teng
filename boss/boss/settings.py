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

'cookie': '_9755xjdesxxd_=32; YD00951578218230%3AWM_TID=TNUb8FbfY%2FJEBFAEAQPVQzBtaJeYRQ8%2B; wt2=DUF_p9BkdsvOOwAUOBMkKzGyZnGM3ghXHZw4IE97Jvc-bCYXBYRmSAqgKLh820nLvtFdARmX7lJcyLTTfVdVh2Q~~; wbg=0; _bl_uid=0ylC14kh6htf31q314w05g3w9v4F; wd_guid=1f214701-3e94-48a0-9e81-9dbfa9c99891; historyState=state; lastCity=100010000; gdxidpyhxdE=aczuO816EDmBjv79%2FEf01uuhHL8oh5E9A3Vco%2FylPm0D9WlyocD9%5CIqohT%5CeflpkSeVqKQnQyaZPBM8o0V1xQJOljTMzfzu7ggqP6bOZA3b1aYZWEGHjMUArfY0V5WzfMnPV6JDTjHgVpsiL8W4%2BPufCPv2nojY%2BI83l21yU%5C8d4thQ0%3A1654852199870; YD00951578218230%3AWM_NI=SRQ61Rsq1TT4YGA9H1QONaS4iSURVPsK4cbIdFBV7f42CpaUHXZl2nrO4mYgGBPvAt3t2NNBaXVriIZpM%2FMD5XDYz7gFRGgAtJOoIryFtvFLwaT9kcb1oxD0pGT6ZSwzcEI%3D; YD00951578218230%3AWM_NIKE=9ca17ae2e6ffcda170e2e6eeb8ce468def9daef325b6ef8ba2d45a878a8f86d85eaf8da4daeb63fceea687fc2af0fea7c3b92a918e9fd7b45ab1afffb5d7409b998fdacb3b93918282d240ab8d9bb3d55cb195fc84e143a89a8eb7b66ef8ee8d91e45f8c88968db166b291fc8edc6d859ea097c480f1acfeafcd4aa3889a93ec439ab083d0d050f7888cbaf93da59a9ea8e64bb8968190cc7abb9abc97c548b5bf9cdaea69a2efa199c73cb4999cd7d959b5a6ada6cc37e2a3; sid=sem_pz_bdpc_dasou_title; Hm_lvt_194df3105ad7148dcf2b98a91b5e727a=1654741845,1654755348,1654756843,1655088625; __g=sem_pz_bdpc_dasou_title; SERVERID=606144fb348bc19e48aededaa626f54e|1655090637|1655090637; acw_tc=0bdd344a16551158896374264e017c6817e08f4c08ca4639174ca1b8c8a7aa; __l=l=%2Fwww.zhipin.com%2Fjob_detail%2F15ae7d7b951033121XZ43d64EFBW.html&r=https%3A%2F%2Fwww.baidu.com%2Fother.php%3Fsc.0s0000aUI6aQ2wUf4al07aHgwzF_68GFwZHH1aUa9_25531oqvzvcVH5JP_4NXJUK1wG9UTa_0aOhdNoWjPmAQ--6d1HhAfuTxPpQPm9LHzV8njj4o5ENM-TDvQ36TDaHs0QXWo9INrGnG6l_o5QkSzlfaDVqsYJcECOvhh9X9QJ0htCYVojQkD2gRzbGC4qnzK17QiKG1AZVR5aLy1GUUUcX2U3.7D_NR2Ar5Od663rj6t8AGSPticrtXFBPrM-kt5QxIW94UhmLmry6S9wiGyAp7BEIu80.TLFWgv-b5HDkrfK1ThPGujYknHb0THY0IAYqmhq1TsKdTvNzgLw4TARqn0K9u7qYXgK-5Hn0IvqzujdBULP10ZFWIWYs0ZNzU7qGujYkPHnvrj64P1fs0Addgv-b5HDYPWcsnWD10AdxpyfqnHDvnWn1PHn0UgwsU7qGujYknW6zP6KsI-qGujYs0A-bm1dcfbR0TA-b5HD0mv-b5H00mLFW5HDsnjbv%26dt%3D1655088621%26wd%3Dboss%26tpl%3Dtpl_12826_27888_0%26l%3D1536889740%26us%3DlinkVersion%253D1%2526compPath%253D10036.0-10032.0%2526label%253D%2525E4%2525B8%2525BB%2525E6%2525A0%252587%2525E9%2525A2%252598%2526linkType%253D%2526linkText%253DBOSS%2525E7%25259B%2525B4%2525E8%252581%252598%2525E2%252580%252594%2525E2%252580%252594%2525E6%252589%2525BE%2525E5%2525B7%2525A5%2525E4%2525BD%25259C%2525EF%2525BC%25258C%2525E4%2525B8%25258ABOSS%2525E7%25259B%2525B4%2525E8%252581%252598%2525EF%2525BC%25258C&g=%2Fwww.zhipin.com%2F%3Fsid%3Dsem_pz_bdpc_dasou_title&s=3&friend_source=0&s=3&friend_source=0; __c=1655088625; __a=81015083.1647099806.1654756840.1655088625.291.10.78.78; Hm_lpvt_194df3105ad7148dcf2b98a91b5e727a=1655116323; __zp_stoken__=d95edCzcWXmpMYx80FEQvbg0xOkJASCp5PzckVjJ2f2MfA0BXJH1zDj8aDXd5DW8hWiZSEj1HfwlsHQYAchRoQyZmDSVNRi9fDWhRT0ENSy5gQRZpWHgafSwOIBR7ZgNqGB9gbDhnVANyIXo%3D; geek_zp_token=V1RdsnFOT901dgXdNsyhwZLyK56DzTxw~~'
}
#SPIDER_MIDDLEWARES = {
#    'boss.middlewares.BossSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
   'boss.middlewares.BossDownloaderMiddleware': 543,
   'boss.middlewares.RandomIPMiddleware': 400,
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


