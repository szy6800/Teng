# -*- coding: utf-8 -*-
import scrapy

import time
import re
from lxml import etree
import copy

from .test import *

 # 加盟公司信息 https://www.admin5.com/browse/130/list_50.shtml

class WjSpider(scrapy.Spider):
    name = 'wj8'
    allowed_domains = ['admin5.com']
    start_urls = ['https://apping.admin5.com/?app=start&controller=project_v2&action=page&callback=jQuery321014981654086389096_1630055634893&page=3&cate_id=0&capital_id=0&keyword=&sort=&_=1630055634895']  # 7

    # def start_requests(self):
    #     for each in index():
    #         cate = each["cate"]
    #         pages = each["pages"]
    #         for p in range(pages):
    #             p = f"{p}" if p else ""
    #             url = f"http://bj.renrenbang.com/{cate}/?tf=f&p={p}"
    #             yield scrapy.Request(url=url, callback=self.parse, dont_filter=True)

    def parse(self, response):
        item = {}
        print(response.text)
        a = re.findall('<.?a.href=.{0,3}"(https.*?)".{0,3}target=',response.text)
        for i in a:
            print('===',i)
    #     list_url = response.xpath('//*[@class="clear_fix bg1"]/a[1]/@href').getall()
    #     for href in list_url:
    #         item['url'] = response.urljoin(href.strip())
    #         yield scrapy.Request(item['url'], callback=self.parse_info, meta={'item': copy.deepcopy(item)},
    #                              dont_filter=True)
    # def parse_info(self, response):
    #     item = response.meta['item']
    #