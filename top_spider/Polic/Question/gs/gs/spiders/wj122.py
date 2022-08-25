# -*- coding: utf-8 -*-
import scrapy

import time
import re
from lxml import etree
import copy
from .wj_text import type_polic,index

 # 创业资讯 https://www.admin5.com/browse/130/list_50.shtml

class WjSpider(scrapy.Spider):
    name = 'wj122'
    allowed_domains = ['govpeoplesearch.net']

    # start_urls = ['http://bj.renrenbang.com/gszc/?tf=f&p={}'.format(i) for i in range(1,5)]  #
    # # start_urls = ['http://bj.renrenbang.com/zhishichanquan/?tf=f&p={}'.format(i) for i in range(1,2)]  #
    def start_requests(self):
        list = [
            'Alabama',
            'Alaska',
            'Arizona',
            'Arkansas',
            'California',
            'Colorado',
            'Connecticut',
            'Delaware',
            'Florida',
            'Georgia',
            'Hawaii',
            'Idaho',
            'Illinois',
            'Indiana',
            'Iowa',
            'Kansas',
            'Kentucky',
            'Louisiana',
            'Maine',
            'Maryland',
            'Massachusetts',
            'Michigan',
            'Minnesota',
            'Mississippi',
            'Missouri',
            'Montana',
            'Nebraska',
            'Nevada',
            'New Hampshire',
            'New Jersey',
            'New Mexico',
            'New York',
            'North Carolina',
            'North Dakota',
            'Ohio',
            'Oklahoma',
            'Oregon',
            'Pennsylvania',
            'Rhode Island',
            'South Carolina',
            'South Dakota',
            'Tennessee',
            'Texas',
            'Utah',
            'Vermont',
            'Virginia',
            'Washington',
            'Washington DC',
            'West Virginia',
            'Wisconsin',
            'Wyoming']

        for i in list:
            item = {}
            ai = re.sub(' ', '-', i)
            item['url'] = f"https://govpeoplesearch.net/{ai}/"
            yield scrapy.Request(url=item['url'], callback=self.parse, dont_filter=True, meta={'item': copy.deepcopy(item)})


    def parse(self, response):

        item = response.meta['item']
        # 标题
        item['phone'] = re.findall('([a-zA-Z\,\s·;]+[\d\(\)-]+\-\d{4})',response.text)

        item['title'] = response.xpath('//*[@class="dbg0pd"]//text()').getall()

        item['title_type'] = response.xpath('//*[@class="dbg0pd"]/following::div[1]/text()').getall()

        item['address'] = response.xpath('//*[@class="dbg0pd"]/following::div[1]/text()').getall()

        item['times'] = response.xpath('//*[@class="rllt__wrapped"]/text()').getall()

        yield item



