# -*- coding: utf-8 -*-

# @Author : 石张毅
# @Site : 中国南方电网
# @introduce:https://www.bidding.csg.cn/zbcg/index.jhtml

import scrapy
import copy
from Qinghai.tools.utils import Utils_
from Qinghai.tools.DB_mysql import *
from Qinghai.tools.re_time import Times
import datetime
from Qinghai.tools.uredis import Redis_DB

class CsgSpider(scrapy.Spider):
    name = 'csg'
    allowed_domains = ['csg.com']
    start_urls = ['http://csg.com/']

    def __init__(self, *args, **kwargs):
        super(CsgSpider, self).__init__()
        self.cates = [
            {"cate": "zbgg", "pages": 8},  # 招标公告
        ]
        self.t = Times()
        self.c_time = datetime.datetime.utcnow() - datetime.timedelta(days=5)

    def start_requests(self):
        for each in self.cates:
            cate = each["cate"]
            pages = each["pages"]
            for p in range(pages):
                p = f"_{p + 1}" if p else ""
                url = f"https://www.bidding.csg.cn/zbcg/index{p}.jhtml"
                yield scrapy.Request(url=url, callback=self.parse, dont_filter=True)

    def parse(self, response):
        # print(response.text)
        item = {}
        # 列表页链接和发布时间
        list_url = response.xpath('//*[@class="Blue"]/following-sibling::a[1]/@href').getall()
        # print(list_url)
        pub_times = response.xpath('//*[@class="Black14 Gray"]/text()').getall()
        # 循环遍历
        for href, pub_time in zip(list_url, pub_times):
            # print(response.urljoin(href))
            item['link'] = response.urljoin(href.strip())

            PUBLISH = self.t.datetimes(pub_time)
            item['publish_time'] = PUBLISH.strftime('%Y-%m-%d')  # 发布时间
            item['uid'] = 'zf' + Utils_.md5_encrypt(item['link'] + item['publish_time'])

            if Redis_DB().Redis_pd(item['uid']) is True:  # 数据去重
                print(item['uid'], '\033[0;35m <=======此数据已采集=======> \033[0m')
                return
            # print(item['link'], item['publish_time'])
            ctime = self.t.datetimes(item['publish_time'])
            # if ctime < self.c_time:
            #     print('文章发布时间大于规定时间，不予采集', item['link'])
            #     return
            yield scrapy.Request(item['link'], callback=self.parse_info, meta={'item': copy.deepcopy(item)},
                                 dont_filter=True)

    def parse_info(self, response):
        if response.status != 200:
            return
        item = response.meta['item']
        # 标题
        item['title'] = response.xpath('//*[@class="s-title"]/text()').get()
        item['uuid'] = ''

        item['intro'] = ''
        item['abs'] = '1'
        from lxml import etree
        html = etree.HTML(response.text)
        div_data = html.xpath('//*[@class="Content"]')
        item['content'] = etree.tostring(div_data[0], encoding='utf-8').decode()
        # 购买人
        item['purchaser'] = ''
        item['create_time'] = str(datetime.datetime.now().strftime('%Y-%m-%d'))
        # 代理人
        item['proxy'] = ''
        item['update_time'] = ''

        item['deleted'] = ''
        # 省 份
        item['province'] = ''
        # 基础
        item['base'] = ''

        item['type'] = response.xpath('//*[@class="W1200 Center Top18"]/a[last()]/text()').get()
        # 行业
        item['items'] = ''
        # 类型编号
        item['data_source'] = '00153'
        item['end_time'] = ''
        item['status'] = ''
        # 采购编号
        item['serial'] = ''

        yield item

