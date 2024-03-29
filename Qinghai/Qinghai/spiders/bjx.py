# -*- coding: utf-8 -*-

# @Author : 石张毅
# @Site :北极星电力新闻网 https://news.bjx.com.cn/list?catid=79


import scrapy
import copy
from Qinghai.tools.utils import Utils_
from Qinghai.tools.DB_mysql import *
from Qinghai.tools.re_time import Times
import datetime
from Qinghai.tools.uredis import Redis_DB

class BjxSpider(scrapy.Spider):
    name = 'bjx'

    def __init__(self, *args, **kwargs ):
        super(BjxSpider, self).__init__()
        self.cates = [
            {"cate": "zbcg", "pages": 4},  # 招标采购


        ]
        self.t = Times()
        self.c_time = datetime.datetime.utcnow() - datetime.timedelta(days=4)

    def start_requests(self):
        for i in range(1,4):
            url = "https://news.bjx.com.cn/zb/{}/".format(i)
            yield scrapy.Request(url=url, callback=self.parse,dont_filter=True)

    def parse(self, response):
        # print(response.text)

        # 列表页链接和发布时间
        list_url = response.xpath('//*[@class="cc-list-content"]/ul/li/a/@href').getall()
        # print(list_url)
        titles = response.xpath('//*[@class="cc-list-content"]/ul/li/a/@title').getall()
        pub_times = response.xpath('//*[@class="cc-list-content"]/ul/li/a/following::span[1]/text()').getall()
        # print(titles,pub_times)
        # 循环遍历
        for href, title, pub_time in zip(list_url, titles, pub_times):
            item = {}
            # print(response.urljoin(href))
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
            # print(item['publish_time'])
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
        div_data = html.xpath('//*[@id="article_cont"]')
        item['content'] = etree.tostring(div_data[0], encoding='utf-8').decode()
        item['purchaser'] = ''
        item['create_time'] = str(datetime.datetime.now().strftime('%Y-%m-%d'))
        item['proxy'] = ''
        item['update_time'] = ''

        item['deleted'] = ''
        item['province'] = ''
        item['base'] = ''
        item['type'] = '招标信息'
        item['items'] = ''
        item['data_source'] = '00127'
        item['end_time'] = ''
        item['status'] = ''
        item['serial'] = ''

        yield item
