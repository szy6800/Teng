# -*- coding: utf-8 -*-

# @Author : 石张毅
# @Site :https://www.mps.gov.cn/n2254314/n2254475/n2254481/index.html 公安部
# @introduce:政府采购

import scrapy
import copy
from Qinghai.tools.utils import Utils_
from Qinghai.tools.DB_mysql import *
from Qinghai.tools.re_time import Times
import datetime


class MpsSpider(scrapy.Spider):
    name = 'mps'
    # allowed_domains = ['mps.gov.cn']
    # start_urls = ['http://mps.gov.cn/']

    def __init__(self, *args, **kwargs ):
        super(MpsSpider, self).__init__()
        self.cates = [


        ]
        self.t = Times()
        self.c_time = datetime.datetime.utcnow() - datetime.timedelta(days=30)

    def start_requests(self):
        url = "https://www.mps.gov.cn/n2254314/n2254475/n2254481/index.html"
        headers={
            "Cookie": "maxPageNum7574611=275; __jsluid_s=e1b2cf13cdcde37873b4ef3f3d9fc6dc; __jsl_clearance_s=1655357406.274|0|PHwCCil8h%2Bpr%2FNcevv6CImMdtf8%3D",
            "Host": "www.mps.gov.cn",
        }
        yield scrapy.Request(url=url, callback=self.parse,dont_filter=True, headers=headers)

    def parse(self, response):
        print(response.text)

        list_url = response.xpath('//*[@class="list"]/li/a/@href').getall()
        # print(list_url)
        pub_times = response.xpath('//*[@class="list"]/li/a/preceding::span[1]/text()').getall()
        #循环遍历
        for href, pub_time in zip(list_url, pub_times):
            item = {}
            # print(response.urljoin(href))
            item['link'] = response.urljoin(href.strip())
            PUBLISH = self.t.datetimes(pub_time)
            item['publish_time'] = PUBLISH.strftime('%Y-%m-%d')  # 发布时间
            print(item['link'], item['publish_time'])
            ctime = self.t.datetimes(item['publish_time'])
            if ctime < self.c_time:
                print('文章发布时间大于规定时间，不予采集', item['link'])
                return
            yield scrapy.Request(item['link'], callback=self.parse_info, meta={'item': copy.deepcopy(item)},dont_filter=True)

    def parse_info(self, response):
        if response.status != 200:
            return
        item = response.meta['item']
        # 标题
        item['uuid'] = ''
        item['title'] = response.xpath('//*[@class="bTitle w915"]/p[1]/text()').get()

        item['uid'] = 'zf' + Utils_.md5_encrypt(item['title'] + item['link'] + item['publish_time'] )
        item['intro'] = ''
        item['abs'] = '1'
        from lxml import etree
        html = etree.HTML(response.text)
        div_data = html.xpath('//*[@id="ztdx"]')
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

        item['type'] = '政府采购'

        # 行业
        item['items'] = ''
        # 类型编号
        item['data_source'] = '00151'
        item['end_time'] = ''
        item['status'] = ''
        # 采购编号
        item['serial'] = ''

        yield item