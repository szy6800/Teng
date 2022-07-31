# -*- coding: utf-8 -*-

# @Time : 2022-07-28 11:06:38
# @Author : 石张毅
# @Site :  http://www.qhbidding.com/zbgg/index.jhtml
# @introduce: 青海发投机电设备招标有限公司

import scrapy
import copy
from Qinghai.tools.utils import Utils_
from Qinghai.tools.DB_mysql import *
from Qinghai.tools.re_time import Times
import datetime
from Qinghai.tools.uredis import Redis_DB


class QhBiddingSpider(scrapy.Spider):
    name = 'qh_bidding'

    def __init__(self, *args, **kwargs):
        super(QhBiddingSpider, self).__init__()
        self.cates = [
            {"cate": "gs", "pages": 2},
            {"cate": "zhbgg", "pages": 2},
            {"cate": "zbgg", "pages": 2},

        ]
        self.t = Times()
        self.c_time = datetime.datetime.utcnow() - datetime.timedelta(days=3)

    def start_requests(self):
        for each in self.cates:
            cate = each["cate"]
            pages = each["pages"]
            for p in range(0, pages):
                p = f"_{p+1}" if p else ""
                url = f"http://www.qhbidding.com/{cate}/index{p}.jhtml"
                # print(url)
                yield scrapy.Request(url=url, callback=self.parse, dont_filter=True)


    def parse(self, response, **kwargs):
        # 列表页链接和发布时间
        count_list = response.xpath('//*[@class="lb-link"]/ul/li')
        if count_list is []:
            return
        for count in count_list:
            item = dict()
            # 列表页链接和发布时间
            item['link'] = response.urljoin(count.xpath('./a/@href').get())
            item['title'] = count.xpath('./a/@title').get()
            if item['title'] is None:
                continue
            pub_time = count.xpath('./a/span[@class="bidDate"]/text()').get()
            PUBLISH = self.t.datetimes(pub_time)
            item['publish_time'] = PUBLISH.strftime('%Y-%m-%d')  # 发布时间
            #print(item['publish_time'],item['link'],item['title'])
            item['uid'] = 'zf' + Utils_.md5_encrypt(item['title'] + item['link'] + item['publish_time'])
            ctime = self.t.datetimes(item['publish_time'])
            if ctime < self.c_time:
                print('文章发布时间大于规定时间，不予采集', item['link'])
                return
            if Redis_DB().Redis_pd(item['uid']) is True:  # 数据去重
                print(item['uid'], '\033[0;35m <=======此数据已采集=======> \033[0m')
                return
            yield scrapy.Request(item['link'], callback=self.parse_info, meta={'item': copy.deepcopy(item)},
                                 dont_filter=True)

    def parse_info(self, response):
        if response.status != 200:
            return
        item = response.meta['item']
        # 标题
        item['uuid'] = ''

        item['intro'] = ''
        item['abs'] = '1'
        from lxml import etree
        html = etree.HTML(response.text)
        div_data = html.xpath('//*[@class="ninfo-con"]')
        item['content'] = etree.tostring(div_data[0], encoding='utf-8').decode()
        item['purchaser'] = ''
        item['create_time'] = str(datetime.datetime.now().strftime('%Y-%m-%d'))
        item['proxy'] = ''
        item['update_time'] = ''
        item['deleted'] = ''
        item['province'] = '青海省'
        item['base'] = ''
        item['type'] = response.xpath('//*[@class="loc-link"]/a[2]/text()').get()
        item['items'] = ''
        item['data_source'] = '00692'
        item['end_time'] = ''
        item['status'] = ''
        item['serial'] = ''
        # print(item)
        yield item
