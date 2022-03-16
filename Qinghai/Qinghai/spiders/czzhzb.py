# -*- coding: utf-8 -*-

# @Author : 石张毅
# @Site :常州正衡招投标有限公司  http://www.czzhzb.com
# @introduce:
import re

import scrapy
import copy
from Qinghai.tools.utils import Utils_
from Qinghai.tools.DB_mysql import *
from Qinghai.tools.re_time import Times
import datetime


class CzzhzbSpider(scrapy.Spider):
    name = 'czzhzb'
    allowed_domains = ['czzhzb.com']
    start_urls = ['http://czzhzb.com/']

    def __init__(self, *args, **kwargs ):
        super(CzzhzbSpider, self).__init__()
        self.cates = [
            {"cate": "1", "pages": 2},  # 招标与采购公告
            {"cate": "11", "pages": 2},  # 补充公告
            {"cate": "3", "pages": 2},  # 中标成交公告


        ]
        self.t = Times()
        self.c_time = datetime.datetime.utcnow() - datetime.timedelta(days=5)

    def start_requests(self):
        for each in self.cates:
            cate = each["cate"]
            pages = each["pages"]
            for p in range(1, pages):
                # p = f"_{p+1}" if p else ""
                url = f"http://www.czzhzb.com/zaobiao/{cate}-{p}.htm"
                yield scrapy.Request(url=url, callback=self.parse,dont_filter=True)

    def parse(self, response):
        # print(response.text)
        item = {}
        # 列表页链接和发布时间
        list_url = response.xpath('//*[@class="zh_zblist_bk"]//a/@href').getall()
        #循环遍历
        for href in list_url:
            # print(response.urljoin(href))
            item['link'] = response.urljoin(href.strip())
            # item['title'] = title.strip()
            # if item['title'] is None:
            #     continue
            # pub_time = re.findall('\\d{4}-\\d{2}-\\d{2}', pub_time)[0]
            # PUBLISH = self.t.datetimes(pub_time)
            # item['publish_time'] = PUBLISH.strftime('%Y-%m-%d')  # 发布时间
            # print(item['publish_time'])
            # ctime = self.t.datetimes(item['publish_time'])
            # if ctime < self.c_time:
            #     print('文章发布时间大于规定时间，不予采集', item['link'])
            #     return
            # print(item['link'])
            yield scrapy.Request(item['link'], callback=self.parse_info, meta={'item': copy.deepcopy(item)},dont_filter=True)

    def parse_info(self, response):
        if response.status != 200:
            return
        item = response.meta['item']
        # 标题
        item['uuid'] = ''
        item['title'] = response.xpath('//*[@class="zh_news_title"]/text()').get().strip()
        print(item['title'])
        item['uid'] = 'zf' + Utils_.md5_encrypt(item['title'] + item['link'] + item['publish_time'] )
        item['intro'] = ''
        item['abs'] = '1'
        item['content'] = response.text
        item['purchaser'] = ''

        pub_time = re.findall('发表时间：(\d{4}-\d{2}-\d{2})', response.text)[0]
        # print(pub_time)
        PUBLISH = self.t.datetimes(pub_time)
        item['publish_time'] = PUBLISH.strftime('%Y-%m-%d')  # 发布时间
        # print(item['publish_time'])
        ctime = self.t.datetimes(item['publish_time'])
        if ctime < self.c_time:
            print('文章发布时间大于规定时间，不予采集', item['link'])
            return
        item['create_time'] = str(datetime.datetime.now().strftime('%Y-%m-%d'))
        item['proxy'] = ''
        item['update_time'] = ''
        item['deleted'] = ''
        item['province'] = ''
        item['base'] = ''
        item['type'] = '招标公告'
        item['items'] = ''
        item['data_source'] = '00144'
        item['end_time'] = ''
        item['status'] = ''
        item['serial'] = ''

        yield item

