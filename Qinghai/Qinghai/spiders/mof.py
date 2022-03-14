# -*- coding: utf-8 -*-

# @Author : 石张毅
# @Site :  财政部 http://www.mof.gov.cn/gkml/xinxi/zhongyangbiaoxun/index.htm
# @introduce: 招标公告 中标公告 更正公告

import scrapy
import copy
from Qinghai.tools.utils import Utils_
from Qinghai.tools.DB_mysql import *
from Qinghai.tools.re_time import Times
import datetime


class MofSpider(scrapy.Spider):
    name = 'mof'
    allowed_domains = ['mof.gov.cn']
    start_urls = ['http://mof.gov.cn/']

    def __init__(self, *args, **kwargs):
        super(MofSpider, self).__init__()
        self.cates = [
            {"cate": "zhongyangzhaobiaogonggao", "pages": 6},  # 招标公告
            {"cate": "zhongyangzhongbiaogonggao", "pages": 6},  # 中标公告
            {"cate": "zhongyanggengzhenggonggao", "pages": 6},  # 更正公告
        ]
        self.t = Times()
        self.c_time = datetime.datetime.utcnow() - datetime.timedelta(days=5)

    def start_requests(self):
        for each in self.cates:
            cate = each["cate"]
            pages = each["pages"]
            for p in range(pages):
                p = f"_{p}" if p else ""
                url = f"http://www.mof.gov.cn/gkml/xinxi/zhongyangbiaoxun/{cate}/index{p}.htm"
                yield scrapy.Request(url=url, callback=self.parse, dont_filter=True)

    def parse(self, response):
        # print(response.text)
        item = {}
        # 列表页链接和发布时间
        list_url = response.xpath('//*[@class="xwbd_lianbolistfrcon"]/li/a/@href').getall()
        # print(list_url)
        titles = response.xpath('//*[@class="xwbd_lianbolistfrcon"]/li/a/@title').getall()
        # print(titles)
        pub_times = response.xpath('//*[@class="xwbd_lianbolistfrcon"]/li/a/following::span[1]/text()').getall()
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
        item['purchaser'] = ''
        item['create_time'] = str(datetime.datetime.now().strftime('%Y-%m-%d'))
        item['proxy'] = ''
        item['update_time'] = ''
        item['deleted'] = ''
        item['province'] = ''
        item['base'] = ''
        if 'zhongyangzhaobiaogonggao' in item['link']:
            item['type'] = '招标公告'
        elif 'zhongyangzhongbiaogonggao' in item['link']:
            item['type'] = '中标公告'
        elif 'zhongyanggengzhenggonggao' in item['link']:
            item['type'] = '更正公告'
        item['items'] = ''
        item['data_source'] = '00136'
        item['end_time'] = ''
        item['status'] = ''
        item['serial'] = ''

        yield item

