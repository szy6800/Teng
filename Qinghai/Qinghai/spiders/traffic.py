# -*- coding: utf-8 -*-
# @Time : 2022/3/3
# @Author : 石张毅
# @site  青海交通局 http://jtyst.qinghai.gov.cn/companynews/gsgg/?pi=

import scrapy
import copy
from lxml import etree
from Qinghai.tools.utils import Utils_
from Qinghai.tools.re_time import Times
import datetime


class TrafficSpider(scrapy.Spider):
    name = 'traffic'
    # allowed_domains = ['qinghai.gov.cn']
    # start_urls = ['http://jtyst.qinghai.gov.cn/companynews/gsgg/?pi={}'.format(i) for i in range(1,2)]

    def __init__(self, *args, **kwargs ):
        super(TrafficSpider, self).__init__()
        self.cates = [
            {"cate": "zbjggs", "pages": 1},  #招标结果公告
            {"cate": "gsgg", "pages": 1},  #公示公告
        ]
        self.t = Times()
        self.c_time = datetime.datetime.utcnow() - datetime.timedelta(days=2)


    def start_requests(self):
        for each in self.cates:
            cate = each["cate"]
            pages = each["pages"]
            for p in range(pages):
                p = f"{p+1}" if p else ""
                url = f"http://jtyst.qinghai.gov.cn/companynews/{cate}/?pi={p}"
                yield scrapy.Request(url=url, callback=self.parse,dont_filter=True)

    def parse(self, response):
        print(response.status)
    #     if response.status != 200:
    #         return None
    #     # print(response.text)
    #     item = {}
    #     # 列表页链接和发布时间
    #     list_url = response.xpath('//*[@class="article_list "]/ul/li/a/@href').getall()
    #     pub_times = response.xpath('//*[@class="article_list "]/ul/li/a/following::span[1]/text()').getall()
    #     # 循环遍历
    #     for href, pub_time in zip(list_url, pub_times):
    #         # print(response.urljoin(href))
    #         item['link'] = response.urljoin(href.strip())
    #         PUBLISH = self.t.datetimes(pub_time[1:-1])
    #         item['publish_time'] = PUBLISH.strftime('%Y-%m-%d')  # 发布时间
    #         ctime = self.t.datetimes(item['publish_time'])
    #
    #         if ctime < self.c_time:
    #             print('文章发布时间大于规定时间，不予采集', item['link'])
    #             return
    #         # print(item['link'], item['publish_time'])
    #         yield scrapy.Request(item['link'], callback=self.parse_info, meta={'item': copy.deepcopy(item)},dont_filter=True)
    #
    # def parse_info(self, response):
    #     if response.status != 200:
    #         return
    #     item = response.meta['item']
    #     # 标题
    #     item['uuid'] = ''
    #     item['title'] = response.xpath("//h1/span//text()").get().strip()
    #
    #     item['uid'] = 'zf' + Utils_.md5_encrypt(item['title'] + item['link'])
    #     item['intro'] = ''
    #     item['abs'] = ''
    #     item['content'] = response.text
    #     item['purchaser'] = ''
    #     item['create_time'] = str(datetime.datetime.now().strftime('%Y-%m-%d'))
    #     item['proxy'] = ''
    #     item['update_time'] = ''
    #     item['deleted'] = ''
    #     item['province'] = '青海省'
    #     item['base'] = ''
    #     if 'zbjggs' in item['link']:
    #         item['type'] ='招标结果公告'
    #     if 'gsgg' in item['link']:
    #         item['type'] = '公示公告'
    #     item['items'] = ''
    #     item['data_source'] = ''
    #     item['end_time'] = ''
    #     item['status'] = ''
    #     item['serial'] = ''
    #
    #     yield item
    #
    #
    #
    #
    #
    #
    #
    #
