# -*- coding: utf-8 -*-

# @Time : 2022-07-12 15:22:07
# @Author : 石张毅
# @Site : https://www.china5e.com/energy-economy/macroeconomy/index_1.html
# https://www.china5e.com/energy-economy/energy-strategy/index_1.html
# https://www.china5e.com/energy-economy/stock/index_2.html
# @introduce:中国能源网

import scrapy
import re
import datetime
import json
import copy
from gansuxinwen.items import GansuxinwenItem
from gansuxinwen.tools.DB_mysql import *
from gansuxinwen.tools.re_time import Times
from gansuxinwen.tools.utils import Utils_
from gansuxinwen.tools.DB_redis import Redis_DB
import scrapy


class China5eSpider(scrapy.Spider):
    name = 'china5e'
    def __init__(self, *args, **kwargs):
        super(China5eSpider, self).__init__()
        self.cates = [
            {"cate": "macroeconomy", "pages": 2},  # 招标公告
            {"cate": "energy-strategy", "pages": 2},  # 招标公告
            {"cate": "stock", "pages": 2},  # 招标公告
        ]
        self.t = Times()
        self.c_time = datetime.datetime.utcnow() - datetime.timedelta(days=2)

    def start_requests(self):
        for each in self.cates:
            cate = each["cate"]
            pages = each["pages"]
            for p in range(1, pages):
                # p = f"_{p + 1}" if p else ""
                url = f"https://www.china5e.com/energy-economy/{cate}/index_{p}.html"
                # print(url)
                yield scrapy.Request(url=url, callback=self.parse, dont_filter=True)

    def parse(self, response, *args):
        count_list = response.xpath('//*[@class="md znw_list_list_height624"]//*[@class="bd"]/ul/li')
        if count_list is []:
            return
        for count in count_list:
            item = GansuxinwenItem()
            # 列表页链接和发布时间
            item['link'] = response.urljoin(count.xpath('./a/@href').get())
            item['title'] = count.xpath('./a/@title').get()
            if item['title'] is None:
                continue
            pub_time = count.xpath('./span/text()').get()
            PUBLISH = self.t.datetimes(pub_time)
            item['publish_time'] = PUBLISH.strftime('%Y-%m-%d')  # 发布
            # print(item['publish_time'],item['link'],item['title'])
            ctime = self.t.datetimes(item['publish_time'])
            if ctime < self.c_time:
                print('文章发布时间大于规定时间，不予采集', item['link'])
                return
            item['uid'] = 'zf' + Utils_.md5_encrypt(item['title'] + item['link'] + item['publish_time'])
            if Redis_DB().Redis_pd(item['uid']) is True:  # 数据去重
                print(item['title'], '\033[0;35m <=======此数据已采集=======> \033[0m')
                break
            item['province'] = ''
            item['create_time'] = str(datetime.datetime.now().strftime('%Y-%m-%d'))
            item['data_source'] = '00672'
            item['status'] = ''
            item['base'] = ''
            yield scrapy.Request(item['link'], callback=self.parse_info, meta={'item': copy.deepcopy(item)},
                                 dont_filter=True)

    def parse_info(self, response):
        # print(response.text)
        if response.status != 200:
            return
        item = response.meta['item']
        # author = re.findall('\d{2}:\d{2}:\d{2}[\n]*(.*?)[&\n]*', response.text)
        # print(author)
        item['author'] = '中国能源网'
        # print(response.text)
        from lxml import etree
        html = etree.HTML(response.text)
        div_data = html.xpath('//*[@class="showcontent"]')
        item['content'] = etree.tostring(div_data[0], encoding='utf-8').decode()
        # print(item)
        yield item

