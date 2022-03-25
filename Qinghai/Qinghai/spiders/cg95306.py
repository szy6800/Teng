# -*- coding: utf-8 -*-

# @Author : 石张毅
# @Site : https://cg.95306.cn/ 国铁采购平台
# @introduce:

import scrapy


class Cg95306Spider(scrapy.Spider):
    name = 'cg95306'
    allowed_domains = ['cg95306.com']
    start_urls = ['http://cg95306.com/']

    def parse(self, response):
        pass
