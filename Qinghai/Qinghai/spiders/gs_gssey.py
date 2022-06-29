# -*- coding: utf-8 -*-

# @Author : 石张毅
# @Site :http://www.gssey.com/news4/index.jhtml
# @introduce: 甘肃省第二人民医院

import scrapy
import scrapy
import copy
from Qinghai.tools.utils import Utils_
from Qinghai.tools.DB_mysql import *
from Qinghai.tools.re_time import Times
from lxml import etree
import datetime
import jsonpath
import json
import re
from Qinghai.tools.uredis import Redis_DB

class GsGsseySpider(scrapy.Spider):
    name = 'gs_gssey'
    def __init__(self, *args, **kwargs ):
        super(GsGsseySpider, self).__init__()
        self.cates = [
            {"cate": "catid=26", "pages": 8},  # 招中标信息
        ]
        self.t = Times()
        self.c_time = datetime.datetime.utcnow() - datetime.timedelta(days=7)

    def start_requests(self):
        for i in range(1, 10):
            url = 'http://www.gssey.com/news4/index_{}.jhtml'.format(i)
            yield scrapy.Request(url=url, callback=self.parse,dont_filter=True)

    def parse(self, response, **kwargs):
        # print(response.text)
        item = {}
        # 列表页链接和发布时间
        list_url = response.xpath('//*[@id="news"]//a[1]/@href').getall()
        titles = response.xpath('//*[@id="news"]//li/a/span/following::text()[2]').getall()
        pub_times = response.xpath('//*[@id="news"]//li/a/span/text()').getall()
        # 循环遍历
        for href, title, pub_time in zip(list_url, titles, pub_times):
            # print(response.urljoin(href))
            item['link'] = response.urljoin(href.strip())
            item['title'] = title.strip()
            if item['title'] is None:
                continue
            PUBLISH = self.t.datetimes(pub_time)
            item['publish_time'] = PUBLISH.strftime('%Y-%m-%d')  # 发布时间
            ctime = self.t.datetimes(item['publish_time'])
            item['uid'] = 'zf' + Utils_.md5_encrypt(item['title'] + item['link'] + item['publish_time'])

            if Redis_DB().Redis_pd(item['uid']) is True:  # 数据去重
                print(item['uid'], '\033[0;35m <=======此数据已采集=======> \033[0m')
                return
            if ctime < self.c_time:
                print('文章发布时间大于规定时间，不予采集', item['link'])
                return
            # print(item['link'], item['publish_time'],item['title'])
            yield scrapy.Request(item['link'], callback=self.parse_info, meta={'item': copy.deepcopy(item)},dont_filter=True)

    def parse_info(self, response):
        if response.status != 200:
            return
        item = response.meta['item']
        # 标题
        item['uuid'] = ''

        item['intro'] = ''
        item['abs'] = '1'
        html = etree.HTML(response.text)
        div_data = html.xpath('//*[@id="ContentArea"]')[0]
        item['content'] =etree.tostring(div_data, encoding='utf-8').decode()
        item['purchaser'] = ''
        item['create_time'] = str(datetime.datetime.now().strftime('%Y-%m-%d'))
        item['proxy'] = ''
        item['update_time'] = ''

        item['deleted'] = ''
        item['province'] = ''
        item['base'] = ''
        item['type'] = '招标公告'
        item['items'] = ''
        item['data_source'] = '00399'
        item['end_time'] = ''
        item['status'] = ''
        item['serial'] = ''

        yield item

