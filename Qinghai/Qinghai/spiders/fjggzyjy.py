# -*- coding: utf-8 -*-

# @Author : 石张毅
# @Site : http://fjggzyjy.cn 福建省公共资源交易网
# @introduce:

import scrapy
import copy
from Qinghai.tools.utils import Utils_
from Qinghai.tools.DB_mysql import *
from Qinghai.tools.re_time import Times
import datetime


class FjggzyjySpider(scrapy.Spider):
    name = 'fjggzyjy'
    # allowed_domains = ['fjggzyjy.com']
    # start_urls = ['http://fjggzyjy.com/']

    def __init__(self, *args, **kwargs ):
        super(FjggzyjySpider, self).__init__()
        self.cates = [
            {"cate": "jyxxzfcg", "pages": 5},  # 招标公告
            {"cate": "jygkgcjs", "pages": 5},  # 招标公告
            {"cate": "jyxxcqgk", "pages": 5},  # 招标公告
            {"cate": "jyxxhjzy", "pages": 5},  # 招标公告
            {"cate": "jyxxylyp", "pages": 1},  # 招标公告
            {"cate": "jyxxother", "pages": 5},  # 招标公告


        ]
        self.t = Times()
        self.c_time = datetime.datetime.utcnow() - datetime.timedelta(days=5)

    def start_requests(self):
        for each in self.cates:
            cate = each["cate"]
            pages = each["pages"]
            for p in range(pages):
                p = f"_{p+1}" if p else ""
                url = f"https://fjggzyjy.cn/{cate}/index{p}.jhtml"
                yield scrapy.Request(url=url, callback=self.parse,dont_filter=True)

    def parse(self, response):
        # print(response.text)
        item = {}
        # 列表页链接和发布时间
        list_url = response.xpath('//*[@class="list-body"]/li//a/@href').getall()

        # print(titles)
        pub_times = response.xpath('//*[@class="list-body"]/li//a/following::p[1]/text()').getall()
        #循环遍历
        for href, pub_time in zip(list_url, pub_times):
            # print(response.urljoin(href))
            item['link'] = response.urljoin(href.strip())
            PUBLISH = self.t.datetimes(pub_time)
            item['publish_time'] = PUBLISH.strftime('%Y-%m-%d')  # 发布时间
            print(item['link'], item['publish_time'])
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
        item['title'] = response.xpath('//*[@class="title"]/p[1]/text()').get().strip()
        item['uid'] = 'zf' + Utils_.md5_encrypt(item['title'] + item['link'])
        item['intro'] = ''
        item['abs'] = ''
        item['content'] = response.text
        item['purchaser'] = ''
        item['create_time'] = str(datetime.datetime.now().strftime('%Y-%m-%d'))
        item['proxy'] = ''
        item['update_time'] = ''
        item['deleted'] = ''
        item['province'] = ''
        item['base'] = ''
        item['type'] = '招标公告'
        item['items'] = ''
        item['data_source'] = '00141'
        item['end_time'] = ''
        item['status'] = ''
        item['serial'] = ''
        yield item
