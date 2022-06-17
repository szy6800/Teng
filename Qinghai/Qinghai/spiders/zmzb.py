# -*- coding: utf-8 -*-

# @Author : 石张毅
# @Site : 中煤招标与采购网 http://www.zmzb.com/cms/index.htm
# @introduce: 招标公告

import scrapy
import copy
from Qinghai.tools.utils import Utils_
from Qinghai.tools.DB_mysql import *
from Qinghai.tools.re_time import Times
import datetime



class ZmzbSpider(scrapy.Spider):
    name = 'zmzb'
    allowed_domains = ['zmzb.com']
    start_urls = ['http://zmzb.com/']

    def __init__(self, *args, **kwargs ):
        super(ZmzbSpider, self).__init__()
        self.cates = [
            {"cate": "ywgg1gc", "pages": 3},  # 招标公告
            {"cate": "ywgg1hw", "pages": 3},  # 中标公告
            {"cate": "ywgg1fw", "pages": 3},  # 中标公告
        ]
        self.t = Times()
        self.c_time = datetime.datetime.utcnow() - datetime.timedelta(days=5)

    def start_requests(self):
        for each in self.cates:
            cate = each["cate"]
            pages = each["pages"]
            for p in range(1, pages):
                # p = f"_{p+1}" if p else ""
                url = f"http://www.zmzb.com/cms/channel/{cate}/index.htm?pageNo={p}"
                yield scrapy.Request(url=url, callback=self.parse,dont_filter=True)

    def parse(self, response):
        # print(response.text)
        item = {}
        # 列表页链接和发布时间
        list_url = response.xpath('//*[@id="list1"]/li/a/@href').getall()
        # print(list_url)
        titles = response.xpath('//*[@id="list1"]/li/a/@title').getall()
        # print(titles)
        pub_times = response.xpath('//*[@id="list1"]/li/a/em[1]/text()').getall()
        #循环遍历
        for href, title, pub_time in zip(list_url, titles, pub_times):
            # print(response.urljoin(href))
            item['link'] = response.urljoin(href.strip())
            item['title'] = title.strip()
            if item['title'] is None:
                continue
            PUBLISH = self.t.datetimes(pub_time.strip())
            item['publish_time'] = PUBLISH.strftime('%Y-%m-%d')  # 发布时间
            # print(item['link'], item['publish_time'],item['title'])
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
        from lxml import etree
        html = etree.HTML(response.text)
        div_data = html.xpath('//*[@class="article-content"]')
        item['content'] = etree.tostring(div_data[0], encoding='utf-8').decode()
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

        item['type'] = response.xpath('//*[@class="loc-link"]/a[2]/text()').get().strip()
        # 行业
        item['items'] = response.xpath('//*[@class="loc-link"]/a[3]/text()').get().strip()
        # 类型编号
        item['data_source'] = '00171'
        item['end_time'] = ''
        item['status'] = ''
        # 采购编号
        item['serial'] = ''

        yield item
