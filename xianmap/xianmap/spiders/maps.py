# -*- coding: utf-8 -*-

# @Author : 石张毅
# @Site : http://www.iecity.com/xian/map/Road---b4e5d7af--1.html
# @introduce:
import copy
import re
import scrapy
import hashlib


class MapsSpider(scrapy.Spider):
    name = 'maps'
    allowed_domains = ['iecity.com']
    # start_urls = ['http://iecity.com/']

    def start_requests(self):
        for i in range(1, 2):
            yield scrapy.Request('http://www.iecity.com/xian/map/Road---b4e5d7af--{}.html'.format(i),
                                 callback=self.parse)

    def parse(self, response, *args, **kwargs):
        # 列表页链接
        list_urls = response.xpath('//ul[@class="MapList clearfix"]/a/@href').getall()
        # 村庄名
        villages = response.xpath('//ul[@class="MapList clearfix"]/a//h3/text()').getall()
        # 县区
        districts = response.xpath('//ul[@class="MapList clearfix"]/a//div/text()').getall()
        # 循环列表
        for href, village, districts in zip(list_urls, villages, districts):
            item = dict()
            item['url'] = response.urljoin(href)
            item['village'] = village
            item['districts'] = districts.replace('地图', '')
            item['province'] = '陕西省'
            item['provincial_capital'] = '西安'
            yield scrapy.Request(item['url'], callback=self.parse_info, meta={'item': copy.deepcopy(item)}, dont_filter=True)

    @staticmethod
    def parse_info(response):
        if response.status != 200:
            return
        item = response.meta['item']
        urls = item['url']
        item['url_md5'] = hashlib.md5(urls.encode(encoding='utf-8')).hexdigest()
        item['lng'] = re.findall('lng=(.*?)&', response.text)[0]
        item['lat'] = re.findall('lat=(.*?)&', response.text)[0]
        yield item

