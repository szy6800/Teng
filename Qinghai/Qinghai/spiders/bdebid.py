# -*- coding: utf-8 -*-

# @Author : 石张毅
# @Site :http://www.bdebid.com 比德电子采购平台
# @introduce: 比德电子采购平台  采购公告 变更公告 候选人公示 采购结果公示

import scrapy
import copy
from Qinghai.tools.utils import Utils_
from Qinghai.tools.DB_mysql import *
from Qinghai.tools.re_time import Times
import datetime


class BdebidSpider(scrapy.Spider):
    name = 'bdebid'
    # allowed_domains = ['bdebid.com']
    # start_urls = ['http://bdebid.com/']

    def __init__(self, *args, **kwargs ):
        super(BdebidSpider, self).__init__()
        self.cates = [
            {"cate": "003001", "pages": 5},  # 采购公告
            {"cate": "003002", "pages": 5},  # 变更公告
            {"cate": "003003", "pages": 5},  # 候选人公示
            {"cate": "003004", "pages": 5},  # 采购结果公示

        ]
        self.t = Times()
        self.c_time = datetime.datetime.utcnow() - datetime.timedelta(days=7)

    def start_requests(self):
        for each in self.cates:
            cate = each["cate"]
            pages = each["pages"]
            for p in range(1, pages):
                if p == 1:
                    p = 'detailpage'
                url = f"https://www.bdebid.com/gggs/{cate}/{p}.html"
                # print(url)
                yield scrapy.Request(url=url, callback=self.parse, dont_filter=True)

    def parse(self, response):
        # print(response.text)
        item = {}
        # 列表页链接和发布时间
        list_url = response.xpath('//*[@class="sub-items"]/li/a/@href').getall()
        # print(list_url)
        titles = response.xpath('//*[@class="sub-items"]/li/a/@title').getall()
        pub_times = response.xpath('//*[@class="sub-items"]/li/a/following::span[1]/text()').getall()
        # print(titles,pub_times)
        # 循环遍历
        for href, title, pub_time in zip(list_url, titles, pub_times):
            # print(response.urljoin(href))
            item['link'] = response.urljoin(href.strip())
            item['title'] = title.strip()
            if item['title'] is None:
                continue
            PUBLISH = self.t.datetimes(pub_time)
            item['publish_time'] = PUBLISH.strftime('%Y-%m-%d')  # 发布时间
            # print(item['publish_time'])
            ctime = self.t.datetimes(item['publish_time'])
            if ctime < self.c_time:
                print('文章发布时间大于规定时间，不予采集', item['link'])
                return
            # print(item['link'], item['publish_time'],item['title'])
            yield scrapy.Request(item['link'], callback=self.parse_info, meta={'item': copy.deepcopy(item)},dont_filter=True)

    @staticmethod
    def parse_info(response):
        if response.status != 200:
            return
        item = response.meta['item']
        # 标题
        item['uuid'] = ''
        # md5操作
        item['uid'] = 'zf' + Utils_.md5_encrypt(item['title'] + item['link'] + item['publish_time'])
        item['intro'] = ''
        item['abs'] = '1'
        from lxml import etree
        html = etree.HTML(response.text)
        div_data = html.xpath('//*[@class="ewb-trade-info"]')
        item['content'] = etree.tostring(div_data[0], encoding='utf-8').decode()
        item['purchaser'] = ''
        item['create_time'] = str(datetime.datetime.now().strftime('%Y-%m-%d'))
        item['proxy'] = ''
        item['update_time'] = ''
        item['deleted'] = ''
        item['province'] = ''
        item['base'] = ''
        if '003001' in item['link']:
            item['type'] = '采购公告'
        elif '003002' in item['link']:
            item['type'] = '变更公告'
        elif '003003' in item['link']:
            item['type'] = '候选人公示'
        elif '003004' in item['link']:
            item['type'] = '采购结果公示'
        item['items'] = ''
        item['data_source'] = '00134'
        item['end_time'] = ''
        item['status'] = ''
        item['serial'] = ''

        yield item

