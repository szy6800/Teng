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


class CcgpgovSpider(scrapy.Spider):
    name = 'ccgpgov'
    # allowed_domains = ['www.c']
    # start_urls = ['http://www.c/']

    def __init__(self, *args, **kwargs,):
        super(CcgpgovSpider, self).__init__()
        self.L = {
            'dfgg': '地方公告',
            'zygg': '中央公告'
        }

        self.t = Times()
        self.conn = conn
        self.cursor = cursor
        self.c_time = datetime.datetime.utcnow() - datetime.timedelta(days=2)

    def start_requests(self):
        for k,v in self.L.items():
            new_url = f'http://www.ccgp.gov.cn/cggg/{k}/'
            page = 0
            yield scrapy.Request(new_url, callback=self.parse, meta={'k':k, 'page':page})

    def parse(self, response, *args):
        # print(response.text)
        k = response.meta['k']
        page = response.meta['page']
        count_list = response.xpath('//div[@class="vF_detail_relcontent_lst"]/ul/li')
        if count_list == []:
            return
        for count in count_list:
            item = ZhaobiaoItem()
            item['uuid'] = ''
            item['title'] = count.xpath('./a/@title').get()
            if item['title'] == None:
                continue
            item['link'] = 'http://www.ccgp.gov.cn/cggg/' + k + count.xpath('./a/@href').get()[1:]
            # item['id'] = ''
            item['uid'] = 'zf' + Utils_.md5_encrypt(item['title'] + item['link'] + item['publish_time'] )
            item['intro'] = ''
            item['abs'] = '1'
            item['content'] = ''
            PUBLISH = self.t.datetimes(count.xpath('./em[2]/text()').get().strip())
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
            try:
                item['province'] = count.xpath('./em[3]/text()').get().strip()
            except:
                item['province'] = ''
            item['base'] = ''
            item['type'] = count.xpath('./em[1]/text()').get().strip()
            item['items'] = ''
            item['data_source'] = '00085'
            item['end_time'] = ''
            item['status'] = ''
            item['serial'] = ''
            # print(item)
            yield scrapy.Request(item['link'], callback=self.son_parse, meta={'item': deepcopy(item)})

        page += 1
        new_url = f'http://www.ccgp.gov.cn/cggg/{k}/index_{str(page)}.htm'
        # print(new_url)
        yield scrapy.Request(new_url, callback=self.parse, meta={'k': k, 'page': page})

    def son_parse(self, response):
        # time.sleep(1)
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