# -*- coding: utf-8 -*-

# @Time : 2022-07-23 15:33:49
# @Author : 石张毅
# @Site :
# @introduce: 猎聘网


import re
import scrapy


class LpjobSpider(scrapy.Spider):
    name = 'lpjob'
    custom_settings = {
        'DOWNLOAD_DELAY':'5',
        'COOKIES_ENABLED': False,
        'DEFAULT_REQUEST_HEADERS': {
            'accept-encoding': 'gzip, deflate, br', 'accept-language': 'zh-CN,zh;q=0.9', 'cache-control': 'no-cache',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36'
        }
    }
    def __init__(self, *args, **kwargs):
        super(LpjobSpider, self).__init__()
        self.ind = ''

        # self.result = dbz()
    def start_requests(self):

        url = 'https://httpbin.org/get'
        yield scrapy.Request(url, callback=self.parse, dont_filter=True, meta={'proxy': 'http://27.128.225.108:22022'})

    def parse(self, response, *args, **kwargs):
        print(response.text)
        yield scrapy.Request(response.url, callback=self.parse,dont_filter=True, meta={'proxy': 'http://27.128.225.108:22022'})
