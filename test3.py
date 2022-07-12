# -*- coding: utf-8 -*-

# @Time : 2022-07-11 15:29:49
# @Author : 石张毅
# @Site : http://www.conch.cn/xxgs/list.aspx
# @introduce: 安徽海螺水泥股份有限公司


import scrapy


class Test3Spider(scrapy.Spider):
    name = 'test3'
    allowed_domains = ['baiduc.com']
    start_urls = ['http://www.gssgxy.cn/index/hyzx/index.html?page=1']

    def parse(self, response):
        print(response.text)
