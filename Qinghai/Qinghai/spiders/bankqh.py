# -*- coding: utf-8 -*-

# @Author : 石张毅
# @Site :  青海银行 http://www.bankqh.com/titlebar/3/index0.htm
# @introduce:00158
import re

import scrapy
import copy

from lxml import etree

from Qinghai.tools.utils import Utils_
from Qinghai.tools.DB_mysql import *
from Qinghai.tools.re_time import Times
import datetime

from Qinghai.tools.uredis import Redis_DB
class BankqhSpider(scrapy.Spider):
    name = 'bankqh'
    allowed_domains = ['bankqh.com']
    start_urls = ['http://bankqh.com/']

    def __init__(self, *args, **kwargs ):
        super(BankqhSpider, self).__init__()
        self.cates = [
            {"cate": "zbgg", "pages": 3},  # 重要公告
        ]
        self.t = Times()
        self.c_time = datetime.datetime.utcnow() - datetime.timedelta(days=8)

    def start_requests(self):
        for each in self.cates:
            cate = each["cate"]
            pages = each["pages"]
            for p in range(0 ,pages):
                # p = f"_{p+1}" if p else ""
                url = f"http://www.bankqh.com/titlebar/3/index{p}.htm"
                yield scrapy.Request(url=url, callback=self.parse,dont_filter=True)

    def parse(self, response):
        # print(response.text)

        # 列表页链接和发布时间
        list_url = response.xpath('//*[@class="detail_title"]//li/a[1]/@href').getall()
        # print(list_url)
        titles = response.xpath('//*[@class="detail_title"]//li/a[1]/text()').getall()
        # print(titles)
        pub_times = response.xpath('//*[@class="detail_title"]//li/a[1]/following::span[1]/text()').getall()
        # print(pub_times,titles)
        #循环遍历
        for href, title, pub_time in zip(list_url, titles, pub_times):
            item = {}
            # print(response.urljoin(href))
            item['link'] = response.urljoin(href.strip())
            item['title'] = title.strip()
            if item['title'] is None:
                continue
            # pub_time = re.findall('\\d{4}年\\d{2}月\\d{2}', pub_time)[0].replace('年', '-').replace('月','-')
            pub_time = re.findall('\\d{4}年\\d{2}月\\d{2}', pub_time)[0].replace('年', '-').replace('月','-')
            PUBLISH = self.t.datetimes(pub_time)
            item['publish_time'] = PUBLISH.strftime('%Y-%m-%d')  # 发布时间
            # print(item['link'], item['publish_time'],item['title'])
            ctime = self.t.datetimes(item['publish_time'])
            if ctime < self.c_time:
                print('文章发布时间大于规定时间，不予采集', item['link'])
                return
            item['uid'] = 'zf' + Utils_.md5_encrypt(item['title'] + item['link'] + item['publish_time'])
            if Redis_DB().Redis_pd(item['uid']) is True:  # 数据去重
                print(item['uid'], '\033[0;35m <=======此数据已采集=======> \033[0m')
                return
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
        div_data = html.xpath('//*[@id="news_detail1"]')
        item['content'] = etree.tostring(div_data[0], encoding='utf-8').decode()
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
        item['type'] = '重要公告'
        # 行业
        item['items'] = ''
        # 类型编号
        item['data_source'] = '00157'
        item['end_time'] = ''
        item['status'] = ''
        # 采购编号
        item['serial'] = ''

        yield item
