# -*- coding: utf-8 -*-

# @Author : 石张毅
# @Site : 北京汇诚金桥国际招标咨询有限公司 http://www.hcjq.net
# @introduce:

import scrapy
import copy
from Qinghai.tools.utils import Utils_
from Qinghai.tools.DB_mysql import *
from Qinghai.tools.re_time import Times
import datetime


class HcjqSpider(scrapy.Spider):
    name = 'hcjq'
    # allowed_domains = ['hcjq.net']
    # start_urls = ['http://hcjq.net/']

    def __init__(self, *args, **kwargs):
        super(HcjqSpider, self).__init__()
        self.cates = [
            {"cate": "jqzb", "pages": 2},  # 招标采购公告
            {"cate": "hqgg", "pages": 3},  # 结果公告
            {"cate": "jqbg", "pages": 3},  # 变更公告

        ]
        self.t = Times()
        self.c_time = datetime.datetime.utcnow() - datetime.timedelta(days=4)

    def start_requests(self):
        for each in self.cates:
            cate = each["cate"]
            pages = each["pages"]
            for p in range(1, pages):
                if p == 1:
                    p = 'index'
                url = f"http://www.hcjq.net/{cate}/{p}.html"
                print(url)
                yield scrapy.Request(url=url, callback=self.parse, dont_filter=True)

    def parse(self, response):
        # print(response.text)
        item = {}
        # 列表页链接和发布时间
        list_url = response.xpath("//*[contains(@href,'cjq.net/html/2022/jqzb')]/@href").getall()
        # print(list_url)
        titles = response.xpath("//*[contains(@href,'cjq.net/html/2022/jqzb')]/@title").getall()
        pub_times = response.xpath("//*[contains(@href,'cjq.net/html/2022/jqzb')]/following::span[1]/text()").getall()
        # print(titles,pub_times)
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
        item['uid'] = 'zf' + Utils_.md5_encrypt(item['title'] + item['link'] + item['publish_time'] )
        item['intro'] = ''
        item['abs'] = '1'
        from lxml import etree
        html = etree.HTML(response.text)
        div_data = html.xpath('//*[@class="article_view"]')
        item['content'] = etree.tostring(div_data[0], encoding='utf-8').decode()
        item['purchaser'] = ''
        item['create_time'] = str(datetime.datetime.now().strftime('%Y-%m-%d'))
        item['proxy'] = ''
        item['update_time'] = ''
        item['deleted'] = ''
        item['province'] = '北京市'
        item['base'] = ''
        item['base'] = ''
        if 'jqzb' in item['link']:
            item['type'] ='招标采购公告'
        if 'hqgg' in item['link']:
            item['type'] = '结果公告'
        if 'jqbg' in item['link']:
            item['type'] = '变更公告'
        item['items'] = ''
        item['data_source'] = '00129'
        item['end_time'] = ''
        item['status'] = ''
        item['serial'] = ''

        yield item



