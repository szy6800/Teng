# -*- coding: utf-8 -*-

# @Author : 石张毅
# @Site : 中国兵器电子招标投标平台 https://www.norincogroup-ebuy.com/
# @introduce: 招标公告
import re

import scrapy
import copy
from Qinghai.tools.utils import Utils_
from Qinghai.tools.DB_mysql import *
from Qinghai.tools.re_time import Times
import datetime


class NorincogroupSpider(scrapy.Spider):
    name = 'norincogroup'
    allowed_domains = ['norincogroup.com']
    start_urls = ['http://norincogroup.com/']

    def __init__(self, *args, **kwargs ):
        super(NorincogroupSpider, self).__init__()
        self.cates = [

        ]
        self.t = Times()
        self.c_time = datetime.datetime.utcnow() - datetime.timedelta(days=15)

    def start_requests(self):
        for i in range(1, 15):
            url = f'https://bid.norincogroup-ebuy.com/retrieve.do?fl=&hy=&dq=&es=1&keyFlag=&packtype=&packtypeCode=&packtypeValue=&packtypeCodeValue=&typflag=&fbdays=0&esly=&validityPeriodFlag=&flag1=&orderby=1&keyConValue=&keyCon=&fbDateStart=&fbDateEnd=&radio=on&ggyxq_time=2022-03-25+17%3A00%3A00&ggyxq_time=2022-03-24+17%3A00%3A00&ggyxq_time=2022-03-24+15%3A00%3A00&ggyxq_time=2022-03-24+17%3A00%3A00&pageNumber={i}&pageSize=10&sortColumns=undefined'
            yield scrapy.Request(url=url, callback=self.parse, dont_filter=True)

    def parse(self, response):
        # print(response.text)
        item = {}
        # 列表页链接和发布时间
        list_url = response.xpath('//*[@class="sldivTitle"]/@href').getall()
        # print(list_url)
        titles = response.xpath('//*[@class="sldivTitle"]/@title').getall()
        # print(titles)
        pub_times = response.xpath('//*[@class="date"]/text()[1]').getall()
        # 省份
        provinces = response.xpath('//*[@class="date"]/text()[last()]').getall()
        # 循环遍历
        for href, title, pub_time, province in zip(list_url, titles, pub_times, provinces):
            # print(response.urljoin(href))
            item['link'] = response.urljoin(href.strip())
            # 省 份
            item['province'] = province
            item['title'] = title.strip()
            if item['title'] is None:
                continue
            pub_time = re.findall('\\d{4}-\\d{2}-\\d{2}', pub_time)[0]
            PUBLISH = self.t.datetimes(pub_time.strip())
            item['publish_time'] = PUBLISH.strftime('%Y-%m-%d')  # 发布时间
            print(item['link'], item['publish_time'],item['title'],item['province'])
            ctime = self.t.datetimes(item['publish_time'])
            if ctime < self.c_time:
                print('文章发布时间大于规定时间，不予采集', item['link'])
                return
            yield scrapy.Request(item['link'], callback=self.parse_info, meta={'item': copy.deepcopy(item)},dont_filter=True)

    @staticmethod
    def parse_info(response):
        if response.status != 200:
            return
        item = response.meta['item']
        # 标题
        item['uuid'] = ''
        item['uid'] = 'zf' + Utils_.md5_encrypt(item['title'] + item['link'] + item['publish_time'])
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

        # 基础
        item['base'] = ''

        item['type'] = response.xpath('//*[@class="zbztb_location"]/a[2]/text()').get()
        # 行业
        item['items'] = ' '.join(response.xpath('//*[@class="tender_info"]/span/text()').getall())
        # 类型编号
        item['data_source'] = '00173'

        item['end_time'] = ''
        item['status'] = ''
        # 采购编号
        item['serial'] = ''
        # print(item)
        yield item


