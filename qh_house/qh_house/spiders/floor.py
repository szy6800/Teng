# -*- coding: utf-8 -*-

# @Author : 石张毅
# @Site :https://www.chinabdc.cn/index.html#/NewHouse/detail?ID=60065998
# @introduce: 房屋建筑楼盘信息 详情页信息

import scrapy


class FloorSpider(scrapy.Spider):
    name = 'floor'
    # allowed_domains = ['a.com']
    # start_urls = ['http://a.com/']

    def parse(self, response):
        pass
