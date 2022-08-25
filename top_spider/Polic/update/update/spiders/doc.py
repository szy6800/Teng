# -*- coding: utf-8 -*-
import scrapy
import copy
import time,re
from lxml import etree

# 合同

class Wj2Spider(scrapy.Spider):
    name = 'doc'
    allowed_domains = ['1ppt.com']
    # start_urls = ['http://www.1ppt.com/word/hetong/']
    start_urls = ['http://www.1ppt.com/moban/jiandangjie/ppt_jiandangjie_{}.html'.format(i) for i in range(1, 2)]

    def parse(self, response):
        item = {}
        list_url = response.xpath('//*[@class="tplist"]/li/a/@href').getall()
        # print(list_url)
        list_img = response.xpath('//*[@class="tplist"]/li/a/img/@src').getall()
        list_tit = response.xpath('//*[@class="tplist"]/li/a/img/@alt').getall()
        # 循环遍历
        for href, img, title in zip(list_url,list_img,list_tit):
            # 原始链接
            item['url'] = response.urljoin(href)
            # 封面链接
            item['coverUrl'] = response.urljoin(img)

            item['title'] = title
            # print(item['url'],item['img'],item['title'])
            yield scrapy.Request(item['url'], callback=self.parse_down, meta={'item': copy.deepcopy(item)})

    def parse_down(self, response):
        item = response.meta['item']
        down_url = response.xpath('//*[@class="downurllist"]/li/a/@href').get()
        # print(response.urljoin(down_url))
        yield scrapy.Request(response.urljoin(down_url), callback=self.parse_info, meta={'item': copy.deepcopy(item)})

    def parse_info(self, response):
        item = response.meta['item']
        # 资源链接
        item['sourceUrl'] = response.xpath('//*[@class="c1"]/a/@href').get()
        # 来源网站
        item['sourceSite'] = '合同'
        # 类型
        item['classId'] = 1

        yield item













