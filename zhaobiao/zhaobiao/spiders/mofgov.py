# -*- coding: utf-8 -*-
import datetime
import json

import scrapy
import re
import time

from copy import deepcopy
from zhaobiao.items import ZhaobiaoItem
from zhaobiao.tools.DB_mysql import *
from zhaobiao.tools.re_time import Times
from zhaobiao.tools.utils import Utils_



class MofgovSpider(scrapy.Spider):
    name = 'mofgov'
    # allowed_domains = ['www.c']
    # start_urls = ['http://www.c/']

    def __init__(self, *args, **kwargs):
        super(MofgovSpider, self).__init__()
        self.L = {
            'difangzhaobiaogonggao': '招标公告',
            'difangzhongbiaogonggao': '中标公告',
            'difanggengzhenggonggao': '更正公告'
        }

        self.t = Times()
        self.conn = conn
        self.cursor = cursor
        self.c_time = datetime.datetime.utcnow() - datetime.timedelta(days=2)

    def start_requests(self):
        for k,v in self.L.items():
            new_url = f'http://www.mof.gov.cn/gkml/xinxi/difangbiaoxun/{k}/'
            page = 0
            yield scrapy.Request(new_url, callback=self.parse, meta={'k':k,'v':v,'page':page})

    def parse(self, response):
        # print(response.text)
        k = response.meta['k']
        v = response.meta['v']
        page = response.meta['page']
        count_list = response.xpath('//div[@class="xwbd_lianbolistfr"]/ul/li')
        for count in count_list:
            item = ZhaobiaoItem()
            item['uuid'] = ''
            item['title'] = count.xpath('./a/@title').get()
            if item['title'] == None:
                continue
            item['link'] = 'http://www.mof.gov.cn/gkml/xinxi/difangbiaoxun/' + k + count.xpath('./a/@href').get()[1:]
            # item['id'] = ''
            item['uid'] = 'zf' + Utils_.md5_encrypt(item['title'] + item['link'])
            item['intro'] = ''
            item['abs'] = ''
            item['content'] = ''
            PUBLISH = self.t.datetimes(count.xpath('./span/text()').get().strip())
            item['publish_time'] = PUBLISH.strftime('%Y-%m-%d')  # 发布时间
            ctime = self.t.datetimes(item['publish_time'])
            # print(item['publishdata'])
            # print(type(item['publishdata']))
            if ctime < self.c_time:
                print('文章不在采集范围内，不予采集', item['link'])
                return
            item['purchaser'] = ''
            item['proxy'] = ''
            # item['create_time'] = item['publish_time']
            item['create_time'] = str(datetime.datetime.now().strftime('%Y-%m-%d'))
            item['update_time'] = ''
            item['deleted'] = ''
            item['province'] = ''
            item['base'] = ''
            item['type'] = v
            item['items'] = ''
            item['data_source'] = '00083'
            item['end_time'] = ''
            item['status'] = ''
            item['serial'] = ''
            # print(item)

            yield scrapy.Request(item['link'], callback=self.son_parse, meta={'item': deepcopy(item)})

        page += 1
        new_url = f'http://www.mof.gov.cn/gkml/xinxi/difangbiaoxun/{k}/index_{str(page)}.htm'
        # print(new_url)
        yield scrapy.Request(new_url, callback=self.parse, meta={'k': k, 'v': v, 'page': page})


    def son_parse(self, response):
        # time.sleep(1)
        if response.status != 200:
            return
        item = response.meta['item']
        # print(response.text)
        item['content'] = response.text
        # print(item)
        time.sleep(1)
        yield item
