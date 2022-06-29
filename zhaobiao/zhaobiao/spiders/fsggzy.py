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


class FsggzySpider(scrapy.Spider):
    name = 'fsggzy'
    # allowed_domains = ['www.c']
    # start_urls = ['http://www.c/']

    def __init__(self, *args, **kwargs):
        super(FsggzySpider, self).__init__()
        self.L = {
            'zbgg': '招标公告',
        }
        self.t = Times()
        self.conn = conn
        self.cursor = cursor
        self.c_time = datetime.datetime.utcnow() - datetime.timedelta(days=2)

    def start_requests(self):
        page = 1
        new_url = 'http://ggzy.foshan.gov.cn/sy/jygg/index.html?1'
        yield scrapy.Request(new_url, callback=self.parse, meta={'page': page})

    def parse(self, response):
        page = response.meta['page']
        count_list = response.xpath('/html/body/div[2]/div[2]/div/div[2]/div/div[2]/ul/li')
        for count in count_list:
            item = ZhaobiaoItem()
            item['uuid'] = ''
            item['title'] = count.xpath('./div/a/text()').get().strip()
            if item['title'] is None:
                continue
            item['link'] = count.xpath('./div/a/@href').get()
            # item['id'] = ''
            item['uid'] = 'zf' + Utils_.md5_encrypt(item['title'] + item['link'] + item['publish_time'] )
            item['intro'] = ''
            item['abs'] = '1'
            item['content'] = ''
            PUBLISH = self.t.datetimes(count.xpath('./span/text()').get().strip())
            item['publish_time'] = PUBLISH.strftime('%Y-%m-%d')  # 发布时间
            ctime = self.t.datetimes(item['publish_time'])
            # print(item['publishdata'])
            # print(type(item['publishdata']))
            if ctime < self.c_time:
                print('文章发布时间大于一个月，不予采集', item['link'])
                return
            item['purchaser'] = ''
            item['proxy'] = ''
            item['create_time'] = str(datetime.datetime.now().strftime('%Y-%m-%d'))
            item['update_time'] = ''
        from Qinghai.tools.uredis import Redis_DB
        if Redis_DB().Redis_pd(item['uid']) is True:  #数据去重
            print(item['uid'], '\033[0;35m <=======此数据已采集=======> \033[0m')
            return
            item['deleted'] = ''
            item['province'] = '佛山市'
            item['base'] = ''
            item['type'] = '交易公告'
            item['items'] = ''
            item['data_source'] = '4[佛山公共资源交易信息化综合平台]'
            item['end_time'] = ''
            item['status'] = ''
            item['serial'] = ''
            # print(item)
            # yield item
            yield scrapy.Request(item['link'], callback=self.son_parse, meta={'item': deepcopy(item)})

        page += 1
        new_url = f'http://ggzy.foshan.gov.cn/sy/jygg/index_{page}.html?1'
        yield scrapy.Request(new_url, callback=self.parse, meta={'page': page})

    def son_parse(self, response):
        time.sleep(1)
        if response.status != 200:
            return
        item = response.meta['item']
        # print(response.text)
        from lxml import etree
        html = etree.HTML(response.text)
        div_data = html.xpath('//*[@id="news_detail1"]')
        item['content'] = etree.tostring(div_data[0], encoding='utf-8').decode()
        # print(item)
        time.sleep(1)
        yield item
