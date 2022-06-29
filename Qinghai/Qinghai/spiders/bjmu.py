    # -*- coding: utf-8 -*-

# @Author : 石张毅
# @Site :http://lab.bjmu.edu.cn/cggg/zbcg/index.htm 北京大学医学部


import scrapy
import copy
from Qinghai.tools.utils import Utils_
from Qinghai.tools.DB_mysql import *
from Qinghai.tools.re_time import Times
import datetime
from Qinghai.tools.uredis import Redis_DB

class BjmuSpider(scrapy.Spider):
    name = 'bjmu'
    # allowed_domains = ['lab.bjmu.edu.cn']
    # start_urls = ['http://lab.bjmu.edu.cn/']

    def __init__(self, *args, **kwargs ):
        super(BjmuSpider, self).__init__()
        self.cates = [
            {"cate": "zbcg", "pages": 1},  # 招标采购
            {"cate": "syly", "pages": 1},  # 单一来源
            {"cate": "zxcg", "pages": 1},  # 自行采购


        ]
        self.t = Times()
        self.c_time = datetime.datetime.utcnow() - datetime.timedelta(days=7)

    def start_requests(self):
        for each in self.cates:
            cate = each["cate"]
            pages = each["pages"]
            for p in range(pages):
                p = f"{p}" if p else ""
                url = f"http://lab.bjmu.edu.cn/cggg/{cate}/index{p}.htm"
                yield scrapy.Request(url=url, callback=self.parse,dont_filter=True)

    def parse(self, response):
        # print(response.text)
        item = {}
        # 列表页链接和发布时间
        list_url = response.xpath('//*[@class="list03"]/li/a/@href').getall()
        # print(list_url)
        titles = response.xpath('//*[@class="list03"]/li/a/text()').getall()
        pub_times = response.xpath('//*[@class="list03"]/li/a/preceding::span[1]/text()').getall()
        # print(titles,pub_times)
        # 循环遍历
        for href, title, pub_time in zip(list_url, titles, pub_times):
            # print(response.urljoin(href))
            item['link'] = response.urljoin(href.strip())
            item['title'] = title.strip()
            if item['title'] is None:
                continue
            PUBLISH = self.t.datetimes(pub_time)

            item['publish_time'] = PUBLISH.strftime('%Y-%m-%d')  # 发布
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
        # md5操作

        item['intro'] = ''
        item['abs'] = '1'
        from lxml import etree
        html = etree.HTML(response.text)
        div_data = html.xpath('//*[@class="article"]')
        item['content'] = etree.tostring(div_data[0], encoding='utf-8').decode()
        item['purchaser'] = ''
        item['create_time'] = str(datetime.datetime.now().strftime('%Y-%m-%d'))
        item['proxy'] = ''
        item['update_time'] = ''

        item['deleted'] = ''
        item['province'] = '北京市'
        item['base'] = ''
        if 'zbcg' in item['link']:
            item['type'] = '招标采购'
        elif 'syly' in item['link']:
            item['type'] = '单一来源'
        elif 'zxcg' in item['link']:
            item['type'] = '自行采购'
        item['items'] = ''
        item['data_source'] = '00126'
        item['end_time'] = ''
        item['status'] = ''
        item['serial'] = ''

        yield item

