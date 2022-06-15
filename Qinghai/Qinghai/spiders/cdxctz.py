# -*- coding: utf-8 -*-

# @Author : 石张毅
# @Site : 成都兴城 http://www.cdxctz.com
# @introduce: 招标公告 投标公告

import scrapy
import copy
from Qinghai.tools.utils import Utils_
from Qinghai.tools.DB_mysql import *
from Qinghai.tools.re_time import Times
import datetime


class CdxctzSpider(scrapy.Spider):
    name = 'cdxctz'
    allowed_domains = ['cdxctz.com']
    start_urls = ['http://cdxctz.com/']

    def __init__(self, *args, **kwargs):
        super(CdxctzSpider, self).__init__()
        self.cates = [
            {"cate": "26", "pages": 3},  # 招标公告
            {"cate": "27", "pages": 3},  # 中标公告

        ]
        self.t = Times()
        self.c_time = datetime.datetime.utcnow() - datetime.timedelta(days=5)

    def start_requests(self):
        for each in self.cates:
            cate = each["cate"]
            pages = each["pages"]
            for p in range(1, pages):
                # p = f"_{p}" if p else ""
                url = f"https://www.cdxctz.com/not.aspx?t={cate}&page={p}"
                yield scrapy.Request(url=url, callback=self.parse, dont_filter=True)

    def parse(self, response):
        # print(response.text)
        item = {}
        # 列表页链接和发布时间
        list_url = response.xpath('//*[@class="notList clearfix"]//a/@href').getall()
        # print(list_url)
        titles = response.xpath('//*[@class="notList clearfix"]//p[@class="nowti"]/text()').getall()
        # print(titles)
        #pub_times = response.xpath('//*[@class="xwbd_lianbolistfrcon"]/li/a/following::span[1]/text()').getall()
        # 循环遍历
        for href, title in zip(list_url, titles):
            # print(response.urljoin(href))
            item['link'] = response.urljoin(href.strip())
            item['title'] = title.strip()
            if item['title'] is None:
                continue

            print(item['link'],item['title'])
            yield scrapy.Request(item['link'], callback=self.parse_info, meta={'item': copy.deepcopy(item)},
                                 dont_filter=True)

    def parse_info(self, response):
        if response.status != 200:
            return
        item = response.meta['item']
        # 标题
        item['uuid'] = ''
        pub_time = response.xpath('//*[@class="d"]/text()').get().strip()
        PUBLISH = self.t.datetimes(pub_time)
        item['publish_time'] = PUBLISH.strftime('%Y-%m-%d')  # 发布时间
        print(item['publish_time'])
        ctime = self.t.datetimes(item['publish_time'])
        if ctime < self.c_time:
            print('文章发布时间大于规定时间，不予采集', item['link'])
            return
        item['uid'] = 'zf' + Utils_.md5_encrypt(item['title'] + item['link'] + item['publish_time'] )
        item['intro'] = ''
        item['abs'] = '1'
        item['content'] = response.text
        item['purchaser'] = ''
        item['create_time'] = str(datetime.datetime.now().strftime('%Y-%m-%d'))
        item['proxy'] = ''
        item['update_time'] = ''
        item['deleted'] = ''

        item['province'] = '四川|成都'
        item['base'] = ''
        if '26' in item['link']:
            item['type'] = '招标公告'
        elif '27' in item['link']:
            item['type'] = '中标公告'
        item['items'] = ''
        item['data_source'] = '00137'
        item['end_time'] = ''
        item['status'] = ''
        item['serial'] = ''

        yield item


