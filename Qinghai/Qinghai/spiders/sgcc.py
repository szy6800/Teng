# -*- coding: utf-8 -*-

# @Author : 石张毅
# @Site : 青海省电力公司 http://www.qh.sgcc.com.cn/html/main/col7/column_7_2.html
# @introduce:通知公告

import copy
from Qinghai.tools.utils import Utils_
from Qinghai.tools.DB_mysql import *
from Qinghai.tools.re_time import Times
import datetime
import scrapy


class SgccSpider(scrapy.Spider):
    name = 'sgcc'
    allowed_domains = ['sgcc.com']
    start_urls = ['http://sgcc.com/']

    def __init__(self, *args, **kwargs ):
        super(SgccSpider, self).__init__()
        self.cates = [
            {"cate": "zbgg", "pages": 3},  # 招标公告

        ]
        self.t = Times()
        self.c_time = datetime.datetime.utcnow() - datetime.timedelta(days=2)

    def start_requests(self):
        for each in self.cates:
            cate = each["cate"]
            pages = each["pages"]
            for p in range(1, pages):
                # p = f"_{p+1}" if p else ""
                url = f"http://www.qh.sgcc.com.cn/html/main/col7/column_7_{p}.html"
                yield scrapy.Request(url=url, callback=self.parse,dont_filter=True)

    def parse(self, response):
        # print(response.text)
        item = {}
        # 列表页链接和发布时间
        list_url = response.xpath('//*[@class="list"]/li/a/@href').getall()
        # print(list_url)
        # titles = response.xpath('//*[@class="lt_title fl zx"]/a[3]/text()').getall()
        # print(titles)
        pub_times = response.xpath('//*[@class="list"]/li/a/following::span[1]/text()').getall()
        #循环遍历
        for href, pub_time in zip(list_url, pub_times):
            # print(response.urljoin(href))
            item['link'] = response.urljoin(href.strip())
            PUBLISH = self.t.datetimes(pub_time)
            item['publish_time'] = PUBLISH.strftime('%Y-%m-%d')  # 发布时间
            # print(item['link'], item['publish_time'])
            ctime = self.t.datetimes(item['publish_time'])
            if ctime < self.c_time:
                print('文章发布时间大于规定时间，不予采集', item['link'])
                return
            yield scrapy.Request(item['link'], callback=self.parse_info, meta={'item': copy.deepcopy(item)},dont_filter=True)

    def parse_info(self, response):
        if response.status != 200:
            return
        item = response.meta['item']
        # 标题
        item['uuid'] = ''
        item['title'] = response.xpath('//h1/span/text()').get()
        item['uid'] = 'zf' + Utils_.md5_encrypt(item['title'] + item['link'] + item['publish_time'] )
        item['intro'] = ''
        item['abs'] = '1'
        item['content'] = response.text
        # 购买人
        item['purchaser'] = ''
        item['create_time'] = str(datetime.datetime.now().strftime('%Y-%m-%d'))
        # 代理人
        item['proxy'] = ''
        item['update_time'] = ''
        item['deleted'] = ''
        # 省 份
        item['province'] = ''
        # 基础
        item['base'] = ''

        item['type'] = '通知公告'
        # 行业
        item['items'] = ''
        # 类型编号
        item['data_source'] = '00159'
        item['end_time'] = ''
        item['status'] = ''
        # 采购编号
        item['serial'] = ''

        yield item
