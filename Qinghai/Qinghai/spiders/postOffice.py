# -*- coding: utf-8 -*-

# @Time : 2022/3/3
# @Author : 石张毅
# @site: 中国邮政 http://qh.chinapost.com.cn/html1/category/18104/822-1.htm

import scrapy
import copy
from Qinghai.tools.utils import Utils_
from Qinghai.tools.DB_mysql import *
from Qinghai.tools.re_time import Times
import datetime


class PostOfficeSpider(scrapy.Spider):

    name = 'postOffice'

    def __init__(self, *args, **kwargs,):
        super(PostOfficeSpider, self).__init__()
        self.cates = [
            {"cate": "html1/category/18104/822", "pages": 2},  #通知公告
        ]

        self.t = Times()
        self.c_time = datetime.datetime.utcnow() - datetime.timedelta(days=2)

    def start_requests(self):
        for each in self.cates:
            cate = each["cate"]
            pages = each["pages"]
            for p in range(1,pages):
                url = f"http://qh.chinapost.com.cn/html1/category/18104/822-{p}.htm"
                yield scrapy.Request(url=url, callback=self.parse, dont_filter=True)


    def parse(self, response):
        # print(response.text)
        item = {}
        # 列表页链接和发布时间
        list_url = response.xpath('//*[@id="ReportIDname"]/a/@href').getall()
        pub_times = response.xpath('//*[@id="ReportIDname"]/a/@href/following::span[1]/text()').getall()
        # 循环遍历
        for href, pub_time in zip(list_url, pub_times):
            # print(response.urljoin(href))
            item['link'] = response.urljoin(href.strip())
            PUBLISH = self.t.datetimes(pub_time)
            item['publish_time'] = PUBLISH.strftime('%Y-%m-%d')  # 发布时间
            ctime = self.t.datetimes(item['publish_time'])

            if ctime < self.c_time:
                print('文章发布时间大于规定时间，不予采集', item['link'])
                return
            print(item['link'], item['publish_time'])
            yield scrapy.Request(item['link'], callback=self.parse_info, meta={'item': copy.deepcopy(item)},
                                 dont_filter=True)



    def parse_info(self, response):
        if response.status != 200:
            return
        item = response.meta['item']
        # 标题
        item['uuid'] = ''
        item['title'] = response.xpath('//span[@id="ReportIDname"]/text()').get().strip()
        item['uid'] = 'zf' + Utils_.md5_encrypt(item['title'] + item['link'] + item['publish_time'] )
        item['intro'] = ''
        item['abs'] = '1'
        item['content'] = response.text
        item['purchaser'] = ''
        item['proxy'] = ''
        item['update_time'] = ''
        item['deleted'] = ''
        item['province'] = '青海省'
        item['base'] = ''
        item['create_time'] = str(datetime.datetime.now().strftime('%Y-%m-%d'))
        item['type'] = '通知公告'
        item['items'] = ''
        item['data_source'] = ''
        item['end_time'] = ''
        item['status'] = ''
        item['serial'] = ''

        yield item
