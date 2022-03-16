# -*- coding: utf-8 -*-

# @Author : 石张毅
# @Site :59医疗器械网 http://www.59med.com/news/list.php?catid=26
# @introduce： 招中标信息

import scrapy
import copy
from Qinghai.tools.utils import Utils_
from Qinghai.tools.DB_mysql import *
from Qinghai.tools.re_time import Times
import datetime


class A59medSpider(scrapy.Spider):
    name = 'a59med'
    # allowed_domains = ['59med.com']
    # start_urls = ['http://59med.com/']

    def __init__(self, *args, **kwargs ):
        super(A59medSpider, self).__init__()
        self.cates = [
            {"cate": "catid=26", "pages": 8},  # 招中标信息

        ]
        self.t = Times()
        self.c_time = datetime.datetime.utcnow() - datetime.timedelta(days=8)

    def start_requests(self):
        for each in self.cates:
            cate = each["cate"]
            pages = each["pages"]
            for p in range(1, pages):
                url = f"http://www.59med.com/news/list.php?{cate}&page={p}"
                yield scrapy.Request(url=url, callback=self.parse,dont_filter=True)

    def parse(self, response):
        # print(response.text)
        item = {}
        # 列表页链接和发布时间
        list_url = response.xpath('//*[@class="catlist"]/ul/li/a/@href').getall()
        titles = response.xpath('//*[@class="catlist"]/ul/li/a/@title').getall()
        pub_times = response.xpath('//*[@class="catlist"]/ul/li/a/@href/preceding::i[1]/text()').getall()
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

            if ctime < self.c_time:
                print('文章发布时间大于规定时间，不予采集', item['link'])
                return
            # print(item['link'], item['publish_time'])
            yield scrapy.Request(item['link'], callback=self.parse_info, meta={'item': copy.deepcopy(item)},dont_filter=True)

    def parse_info(self, response):
        if response.status != 200:
            return
        item = response.meta['item']
        # 标题
        item['uuid'] = ''
        item['uid'] = 'zf' + Utils_.md5_encrypt(item['title'] + item['link'] + item['publish_time'] )
        item['intro'] = ''
        item['abs'] = '1'
        item['content'] = response.text
        item['purchaser'] = ''
        item['create_time'] = str(datetime.datetime.now().strftime('%Y-%m-%d'))
        item['proxy'] = ''
        item['update_time'] = ''
        item['deleted'] = ''
        item['province'] = ''
        item['base'] = ''
        item['type'] = '招中标信息'
        item['items'] = ''
        item['data_source'] = '00119'
        item['end_time'] = ''
        item['status'] = ''
        item['serial'] = ''

        yield item
