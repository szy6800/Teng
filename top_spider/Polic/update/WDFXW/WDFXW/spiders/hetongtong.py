# -*- coding: utf-8 -*-
import requests
import scrapy
import copy
import time, re
from lxml import etree

# 财务报表 http://m.wdfxw.net/pro1009Grade2QPage1.htm

class Wj2Spider(scrapy.Spider):
    name = 'hetongtong'
    allowed_domains = ['hetongdoc.com']
    start_urls = ['http://hetongdoc.com/node/search.html?cond=%E5%90%88%E5%90%8C%E7%BD%91&utm_source=baiduzc2&utm_medium=ht-hxc-PC&utm_campaign=hzht-507&utm_term=htw&bd_vid=10924753689856081484']
    # print(start_urls)

    def parse(self, response):
        item = {}
        list_codes = response.xpath('//*[@class="jsListItemClick"]/@data-fileid').getall()
        titles = response.xpath('//*[@class="jsListItemClick"]/@data-filename').getall()
        imgs = response.xpath('//*[@class="jsListItemClick"]//img/@src').getall()
        # 循环遍历
        for href, title, img in zip(list_codes, titles, imgs):
            # 原始链接
            item['url'] = "http://hetongdoc.com/f/"+href +".html"
            item['title'] = title
            item['img'] = response.urljoin(img)
            yield scrapy.Request(item['url'], callback=self.parse_down, meta={'item': copy.deepcopy(item)})

    def parse_down(self, response):
        item = response.meta['item']
        down_url = re.findall('https:\/\/swf.ishare.down.sina.com.cn\/.*?\?ssig=.*?&Expires=\d+&KID=.*?,ishare&range=[0-9-]+', response.text)
        for i in down_url:
            print(i)
            # res = requests.get(i,timeout=0.5)
            # item['content'] = res.text
            # yield item
    #     item['title'] = response.xpath('//h1/text()').get()
    #     # print(response.urljoin(down_url))
    #     yield scrapy.Request(response.urljoin(down_url), callback=self.parse_info, meta={'item': copy.deepcopy(item)})
    #
    # def parse_info(self, response):
    #     item = response.meta['item']
    #     # 资源链接
    #     item['sourceUrl'] = response.urljoin(response.xpath('//*[@class="maininfo"]/a/@href').get())
    #     # 来源网站
    #     item['sourceSite'] = 'WDFXW文档分享网'
    #     # 类型
    #     item['classId'] = 56
    #
    #     yield item

    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
