# -*- coding: utf-8 -*-

# @Author : 石张毅
# @Site : http://www.gsei.com.cn/html/1336/
# @introduce:甘肃经济信息网

import scrapy
import scrapy
import copy
from Qinghai.tools.utils import Utils_
from Qinghai.tools.DB_mysql import *
from Qinghai.tools.re_time import Times
from lxml import etree
import datetime
import jsonpath
import json
from Qinghai.tools.uredis import Redis_DB

class GsGgzySpider(scrapy.Spider):
    name = 'gs_gsei'

    def __init__(self, *args, **kwargs):
        super(GsGgzySpider, self).__init__()
        self.cates = [
            {"cate": "1337", "pages": 3},  #

        ]
        self.t = Times()
        self.c_time = datetime.datetime.utcnow() - datetime.timedelta(days=2)

    def start_requests(self):
        for each in self.cates:
            cate = each["cate"]
            pages = each["pages"]
            for p in range(pages):
                p = f"list-{p + 1}.html" if p else ""
                url = f"http://www.gsei.com.cn/html/{cate}/{p}"
                yield scrapy.Request(url=url, callback=self.parse, dont_filter=True)

    def parse(self, response, **kwargs):
        # print(response.text)

        # 列表页链接和发布时间
        list_url = response.xpath('//*[@class="adaplist94"]/li/a/@href').getall()
        # print(list_url)
        titles = response.xpath('//*[@class="adaplist94"]/li/a/@title').getall()
        pub_times = response.xpath('//*[@class="adaplist94"]/li/a/following::span[1]/text()').getall()
        # print(titles,pub_times)
        # 循环遍历
        for href, title, pub_time in zip(list_url, titles, pub_times):
            item = {}
            item['link'] = response.urljoin(href.strip())
            item['title'] = title.strip()
            if item['title'] is None:
                continue
            PUBLISH = self.t.datetimes(pub_time)
            item['publish_time'] = PUBLISH.strftime('%Y-%m-%d')  # 发布时间
            item['uid'] = 'zf' + Utils_.md5_encrypt(item['title'] + item['link'] + item['publish_time'])
            if Redis_DB().Redis_pd(item['uid']) is True:  # 数据去重
                print(item['uid'], '\033[0;35m <=======此数据已采集=======> \033[0m')
                return
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

        item['intro'] = ''
        item['abs'] = '1'
        from lxml import etree
        html = etree.HTML(response.text)
        div_data = html.xpath('//*[@class="artcon"]')
        item['content'] = etree.tostring(div_data[0], encoding='utf-8').decode()
        item['purchaser'] = ''
        item['create_time'] = str(datetime.datetime.now().strftime('%Y-%m-%d'))
        item['proxy'] = ''
        item['update_time'] = ''

        item['deleted'] = ''
        item['province'] = '甘肃省'
        item['base'] = ''
        item['type'] =response.xpath('//*[@class="position5 pull-left"]/a[3]/text()').get()
        item['items'] = ''
        item['data_source'] = '00543'
        item['end_time'] = ''
        item['status'] = ''
        item['serial'] = ''

        yield item

