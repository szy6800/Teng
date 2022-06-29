# -*- coding: utf-8 -*-

# @Author : 石张毅
# @Site :  http://www.qhheart.com/index.php?c=category&id=18
# @introduce: 招标公告

import scrapy
import copy
from Qinghai.tools.utils import Utils_
from Qinghai.tools.DB_mysql import *
from Qinghai.tools.re_time import Times
import datetime
from Qinghai.tools.uredis import Redis_DB


class QhheartSpider(scrapy.Spider):
    name = 'qhheart'
    allowed_domains = ['qhheart.com']
    start_urls = ['http://qhheart.com/']

    def __init__(self, *args, **kwargs):
        super(QhheartSpider, self).__init__()
        self.cates = [
            {"cate": "8", "pages": 1},  # 招标公告
            {"cate": "8", "pages": 1},  # 招标公告
            {"cate": "8", "pages": 1},  # 招标公告
        ]
        self.t = Times()
        self.c_time = datetime.datetime.utcnow() - datetime.timedelta(days=15)

    def start_requests(self):
        url = f"http://www.qhheart.com/index.php?c=category&id=18"
        yield scrapy.Request(url=url, callback=self.parse, dont_filter=True)

    def parse(self, response):
        # print(response.text)
        item = {}
        # 列表页链接和发布时间
        list_url = response.xpath('//*[@class="list-new mt20"]/ul/li/a/@href').getall()
        # print(list_url)
        titles = response.xpath('//*[@class="list-new mt20"]/ul/li/a/text()').getall()
        # print(titles)
        pub_times = response.xpath('//*[@class="list-new mt20"]/ul/li/a/following::span[1]/text()').getall()
        # 循环遍历
        item['type'] = '通知公告'
        for href, title, pub_time in zip(list_url, titles, pub_times):
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

    @staticmethod
    def parse_info(response):
        if response.status != 200:
            return
        item = response.meta['item']
        # 标题
        item['uuid'] = ''

        item['intro'] = ''
        item['abs'] = '1'
        from lxml import etree
        html = etree.HTML(response.text)
        div_data = html.xpath('//*[@id="scon"]')
        item['content'] = etree.tostring(div_data[0], encoding='utf-8').decode()
        # 购买人
        item['purchaser'] = ''
        item['create_time'] = str(datetime.datetime.now().strftime('%Y-%m-%d'))
        # 代理人
        item['proxy'] = ''
        item['update_time'] = ''

        item['deleted'] = ''
        # 省 份
        item['province'] = '青海省'
        # 基础
        item['base'] = ''
        # 行业
        item['items'] = ''
        # 类型编号
        item['data_source'] = '00170'
        item['end_time'] = ''
        item['status'] = ''
        # 采购编号
        item['serial'] = ''

        yield item
