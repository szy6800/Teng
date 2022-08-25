# -*- coding: utf-8 -*-
import scrapy
import copy
import time, re
from lxml import etree

# 财务报表 http://m.wdfxw.net/pro1009Grade2QPage1.htm

class Wj2Spider(scrapy.Spider):
    name = 'doc'
    allowed_domains = ['m.wdfxw.net']
    start_urls = ['http://m.wdfxw.net/pro1327Grade2QPage{}.htm'.format(i) for i in range(3,10)]
    # print(start_urls)

    def parse(self, response):
        item = {}
        list_url = response.xpath('//*[@class="one"]/a/@href').getall()
        # print(list_url)
        # list_img = ''
        item['coverUrl'] = ''
        # list_tit = response.xpath('//*[@class="one"]/a/@title').getall()
        # 循环遍历
        for href in list_url:
            # 原始链接
            item['url'] = response.urljoin(href)
            # 封面链接
            # item['title'] = title
            # print(item['url'],item['img'],item['title'])
            yield scrapy.Request(item['url'], callback=self.parse_down, meta={'item': copy.deepcopy(item)})

    def parse_down(self, response):
        item = response.meta['item']
        down_url = response.xpath('//*[@class="docinfo"]//a[contains(@href,"Fulltext")]/@href').get()
        item['title'] = response.xpath('//h1/text()').get()
        # print(response.urljoin(down_url))
        yield scrapy.Request(response.urljoin(down_url), callback=self.parse_info, meta={'item': copy.deepcopy(item)})

    def parse_info(self, response):
        item = response.meta['item']
        # 资源链接
        item['sourceUrl'] = response.urljoin(response.xpath('//*[@class="maininfo"]/a/@href').get())
        # 来源网站
        item['sourceSite'] = 'WDFXW文档分享网'
        # 类型
        item['classId'] = 102

        yield item













