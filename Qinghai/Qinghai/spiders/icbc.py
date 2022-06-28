# -*- coding: utf-8 -*-

# @Author : 石张毅
# @Site : 青海分行-中国工商银行
# http://www.gd.icbc.com.cn/icbc/%E9%9D%92%E6%B5%B7%E5%88%86%E8%A1%8C/%E6%9C%80%E6%96%B0%E4%B8%9A%E5%8A%A1/%E9%9B%86%E4%B8%AD%E9%87%87%E8%B4%AD%E4%BF%A1%E6%81%AF%E5%85%AC%E5%BC%80/
# @introduce:  集中采购信息公开
import re

import scrapy
import copy
from Qinghai.tools.utils import Utils_
from Qinghai.tools.DB_mysql import *
from Qinghai.tools.re_time import Times
import datetime


class IcbcSpider(scrapy.Spider):
    name = 'icbc'
    allowed_domains = ['icbc.com']
    start_urls = ['http://icbc.com/']

    def __init__(self, *args, **kwargs ):
        super(IcbcSpider, self).__init__()
        self.cates = [

        ]
        self.t = Times()
        self.c_time = datetime.datetime.utcnow() - datetime.timedelta(days=2)

    def start_requests(self):
        url = f"http://www.gd.icbc.com.cn/icbc/%e9%9d%92%e6%b5%b7%e5%88%86%e8%a1%8c/" \
              f"%e6%9c%80%e6%96%b0%e4%b8%9a%e5%8a%a1/%e9%9b%86%e4%b8%ad%e9%87%87%e8%b4%ad%" \
              f"e4%bf%a1%e6%81%af%e5%85%ac%e5%bc%80/default.htm"

        yield scrapy.Request(url=url, callback=self.parse, dont_filter=True)

    def parse(self, response):
        # print(response.text)
        item = {}
        # 列表页链接和发布时间
        list_url = response.xpath('//*[@class="ChannelSummaryList-insty"]/a/@href').getall()
        # print(list_url)
        titles = response.xpath('//*[@class="ChannelSummaryList-insty"]/a/text()').getall()
        # print(titles)
        #pub_times = response.xpath('//*[@class="column-list-down"]/ul/li/a/following::span[1]/a/text()').getall()
        #循环遍历
        item['type'] = '集中采购信息公开'

        for href, title in zip(list_url, titles):
            # print(response.urljoin(href))
            item['link'] = response.urljoin(href.strip())
            item['title'] = title.strip()
            if item['title'] is None:
                continue
            yield scrapy.Request(item['link'], callback=self.parse_info, meta={'item': copy.deepcopy(item)},
                                 dont_filter=True)

    def parse_info(self, response):
        if response.status != 200:
            return
        item = response.meta['item']
        # 标题
        item['uuid'] = ''
        pub_time = response.xpath('//*[@id="InfoPickFromFieldControl"]/text()').get()

        pub_time = re.findall('\\d{4}-\\d{2}-\\d{2}', pub_time)[0]
        if pub_time is None:
            item['publish_time'] = ''
        else:
            PUBLISH = self.t.datetimes(pub_time)
            item['publish_time'] = PUBLISH.strftime('%Y-%m-%d')  # 发布时间
        ctime = self.t.datetimes(item['publish_time'])
        if ctime < self.c_time:
            print('文章发布时间大于规定时间，不予采集', item['link'])
            return
        item['uid'] = 'zf' + Utils_.md5_encrypt(item['title'] + item['link'] + item['publish_time'])
        item['intro'] = ''
        item['abs'] = '1'
        from lxml import etree
        html = etree.HTML(response.text)
        div_data = html.xpath('//*[@id="mypagehtmlcontent"]')
        item['content'] = etree.tostring(div_data[0], encoding='utf-8').decode()
        # 购买人
        item['purchaser'] = ''
        item['create_time'] = str(datetime.datetime.now().strftime('%Y-%m-%d'))
        # 代理人
        item['proxy'] = ''
        item['update_time'] = ''
        from Qinghai.tools.uredis import Redis_DB
        if Redis_DB().Redis_pd(item['uid']) is True:  #数据去重
            print(item['uid'], '\033[0;35m <=======此数据已采集=======> \033[0m')
            return
        item['deleted'] = ''
        # 省 份
        item['province'] = '青海省'
        # 基础
        item['base'] = ''
        # 行业
        item['items'] = ''
        # 类型编号
        item['data_source'] = '00166'
        item['end_time'] = ''
        item['status'] = ''
        # 采购编号
        item['serial'] = ''

        yield item
