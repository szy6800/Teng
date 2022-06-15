# -*- coding: utf-8 -*-

# @Author : 石张毅
# @Site :青海省第四人民医院 http://www.qh4yy.com/NewsClass.asp?BigClass=%D5%D0%B1%EA%D0%C5%CF%A2
# @introduce:招标信息
import re

import scrapy
import scrapy
import copy
from Qinghai.tools.utils import Utils_
from Qinghai.tools.DB_mysql import *
from Qinghai.tools.re_time import Times
import datetime


class Qh4yySpider(scrapy.Spider):
    name = 'qh4yy'
    allowed_domains = ['qh4yy.com']
    start_urls = ['http://qh4yy.com/']

    def __init__(self, *args, **kwargs):

        super(Qh4yySpider, self).__init__()
        self.cates = [
            {"cate": "zbgg", "pages": 2},  # 招标公告

        ]
        self.t = Times()
        self.c_time = datetime.datetime.utcnow() - datetime.timedelta(days=3)

    def start_requests(self):
        for each in self.cates:
            cate = each["cate"]
            pages = each["pages"]
            for p in range(1, pages):
                # p = f"_{p+1}" if p else ""
                url = f"http://www.qh4yy.com/NewsClass.asp?BigClass=%D5%D0%B1%EA%D0%C5%CF%A2&SmallClass=&page={p}"
                yield scrapy.Request(url=url, callback=self.parse, dont_filter=True)

    def parse(self, response):
        # print(response.text)
        item = {}
        # 列表页链接和发布时间和标题
        list_url = response.xpath("//*[contains(@href,'shownews.asp?id=')]/@href").getall()
        # print(list_url)
        titles = response.xpath("//*[contains(@href,'shownews.asp?id=')]/text()").getall()
        # print(titles)
        pub_times = response.xpath("//*[contains(text(),'(点击')]/text()[1]").getall()
        # print(pub_times)
        item['type'] = '招标信息'
        # print(item['type'])
        # 循环遍历
        for href, title, pub_time in zip(list_url, titles, pub_times):
            # print(response.urljoin(href))
            item['link'] = response.urljoin(href.strip())
            item['title'] = title.strip()
            if item['title'] is None:
                continue
            pub_time = re.findall('\\d{4}/\\d{1,2}/\\d{1,2}', pub_time)[0]
            PUBLISH = self.t.datetimes(pub_time)
            item['publish_time'] = PUBLISH.strftime('%Y-%m-%d')  # 发布时间
            print(item['link'], item['publish_time'], item['title'], item['type'])
            ctime = self.t.datetimes(item['publish_time'])
            if ctime < self.c_time:
                print('文章发布时间 大于规定时间，不予采集', item['link'])
                return
            yield scrapy.Request(item['link'], callback=self.parse_info, meta={'item': copy.deepcopy(item)},
                                 dont_filter=True)

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
        # 购买人
        item['purchaser'] = ''
        item['create_time'] = str(datetime.datetime.now().strftime('%Y-%m-%d'))
        # 代理人
        item['proxy'] = ''
        item['update_time'] = ''
        item['deleted'] = ''
        # 省 份
        item['province'] = '青海省'
        # 基础
        item['base'] = ''
        # 行业
        item['items'] = ''
        # 类型编号
        item['data_source'] = '00156'
        # 截止时间
        item['end_time'] = ''
        item['status'] = ''
        # 采购编号
        item['serial'] = ''

        yield item
