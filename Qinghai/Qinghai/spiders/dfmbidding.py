# -*- coding: utf-8 -*-

# @Author : 石张毅
# @Site :东方汽车集团有限公司  http://jyzx.dfmbidding.com/zbxx/index.jhtml
# @introduce: 招标公告

import scrapy
import scrapy
import copy
from Qinghai.tools.utils import Utils_
from Qinghai.tools.DB_mysql import *
from Qinghai.tools.re_time import Times
import datetime
from Qinghai.tools.uredis import Redis_DB

class DfmbiddingSpider(scrapy.Spider):
    name = 'dfmbidding'
    allowed_domains = ['dfmbidding.com']
    start_urls = ['http://dfmbidding.com/']

    def __init__(self, *args, **kwargs ):
        super(DfmbiddingSpider, self).__init__()
        self.cates = [
            {"cate": "zbgg", "pages": 1},  # 招标公告


        ]
        self.t = Times()
        self.c_time = datetime.datetime.utcnow() - datetime.timedelta(days=5)

    def start_requests(self):
        for each in self.cates:
            cate = each["cate"]
            pages = each["pages"]
            for p in range(pages):
                p = f"_{p+1}" if p else ""
                url = f"http://jyzx.dfmbidding.com/zbxx/index.jhtml"
                yield scrapy.Request(url=url, callback=self.parse,dont_filter=True)

    def parse(self, response):
        # print(response.text)

        # 列表页链接和发布时间
        list_url = response.xpath('//*[@class="lb-link"]/ul/li/a/@href').getall()
        # print(list_url)
        titles = response.xpath('//*[@class="lb-link"]/ul/li/a/@title').getall()
        # print(titles)
        pub_times = response.xpath('//*[@class="bidDate"]/text()').getall()
        #循环遍历
        for href, title, pub_time in zip(list_url, titles, pub_times):
            # print(response.urljoin(href))
            item = {}
            item['link'] = response.urljoin(href.strip())
            item['title'] = title.strip()
            if item['title'] is None:
                continue
            PUBLISH = self.t.datetimes(pub_time)
            item['publish_time'] = PUBLISH.strftime('%Y-%m-%d')  # 发布时间
            item['uid'] = 'zf' + Utils_.md5_encrypt(item['title'] + item['link'] + item['publish_time'])
            # print(item['publish_time'])

            if Redis_DB().Redis_pd(item['uid']) is True:  # 数据去重
                print(item['uid'], '\033[0;35m <=======此数据已采集=======> \033[0m')
                return
            ctime = self.t.datetimes(item['publish_time'])
            if ctime < self.c_time:
                print('文章发布时间大于规定时间，不予采集', item['link'])
                return
            # print(item['link'], item['publish_time'],item['title'])
            yield scrapy.Request(item['link'], callback=self.parse_info, meta={'item': copy.deepcopy(item)},dont_filter=True)

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
        item['province'] = ''
        item['base'] = ''
        item['type'] = response.xpath('//*[@class="loc-link"]/a[last()-1]/text()').get()
        item['items'] = response.xpath('//*[@class="loc-link"]/a[last()]/text()').get()
        item['data_source'] = '00139'
        item['end_time'] = ''
        item['status'] = ''
        item['serial'] = ''

        yield item

