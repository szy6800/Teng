# -*- coding: utf-8 -*-

# @Author : 石张毅
# @Site :https://buy.cnooc.com.cn/cbjyweb/001/001003/moreinfo.html  中国石油集团有限公司
# @introduce:

import scrapy
import copy
from Qinghai.tools.utils import Utils_
from Qinghai.tools.DB_mysql import *
from Qinghai.tools.re_time import Times
import datetime


class CnoocSpider(scrapy.Spider):
    name = 'cnooc'
    allowed_domains = ['cnooc.com']
    start_urls = ['http://cnooc.com/']

    def __init__(self, *args, **kwargs):
        super(CnoocSpider, self).__init__()
        self.cates = [

            {"cate": "001001", "pages": 8},  # 招标公告
            {"cate": "001002", "pages": 8},  # 中标公示
            {"cate": "001003", "pages": 8},  # 结果公告
            {"cate": "001004", "pages": 8},  # 非招标公告

        ]
        self.t = Times()
        self.c_time = datetime.datetime.utcnow() - datetime.timedelta(days=3)

    def start_requests(self):
        for each in self.cates:
            cate = each["cate"]
            pages = each["pages"]
            for p in range(1, pages):
                # p = f"_{p + 1}" if p else ""
                url = f"https://buy.cnooc.com.cn/cbjyweb/001/{cate}/{p}.html"
                yield scrapy.Request(url=url, callback=self.parse, dont_filter=True)

    def parse(self, response):
        # print(response.text)
        item = {}
        # 列表页链接和发布时间
        list_url = response.xpath('//*[@class="now-hd-items clearfix"]/a/@href').getall()
        # print(list_url)
        titles = response.xpath('//*[@class="now-hd-items clearfix"]/a/@title').getall()
        # print(titles)
        pub_times = response.xpath('//*[@class="now-hd-items clearfix"]/a/following::span[1]/text()').getall()
        # 循环遍历
        for href, title, pub_time in zip(list_url, titles, pub_times):
            # print(response.urljoin(href))
            item['link'] = response.urljoin(href.strip())
            item['title'] = title.strip()
            if item['title'] is None:
                continue
            PUBLISH = self.t.datetimes(pub_time)
            item['publish_time'] = PUBLISH.strftime('%Y-%m-%d')  # 发布时间
            # print(item['link'], item['publish_time'], item['title'])
            ctime = self.t.datetimes(item['publish_time'])
            if ctime < self.c_time:
                print('文章发布时间大于规定时间，不予采集', item['link'])
                return
            yield scrapy.Request(item['link'], callback=self.parse_info, meta={'item': copy.deepcopy(item)},
                                 dont_filter=True)

    def parse_info(self, response):
        if response.status != 200:
            return
        item = response.meta['item']
        # 标题
        item['uuid'] = ''
        item['uid'] = 'zf' + Utils_.md5_encrypt(item['title'] + item['link'])
        item['intro'] = ''
        item['abs'] = ''
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
        if '001001' in item['link']:
            item['type'] = '招标公告'
        elif '001002' in item['link']:
            item['type'] = '中标公示'
        elif '001003' in item['link']:
            item['type'] = '结果公告'
        elif '001004' in item['link']:
            item['type'] = '非招标公告'
        # 行业
        item['items'] = ''
        # 类型编号
        item['data_source'] = '00152'

        item['end_time'] = ''

        item['status'] = ''
        # 采购编号
        item['serial'] = ''

        yield item

