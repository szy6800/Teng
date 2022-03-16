# -*- coding: utf-8 -*-

# @Author : 石张毅
# @Site :北京市海淀区人民政府  http://www.bjhd.gov.cn/zfcg/
# @introduce:
import re

import scrapy
import copy
from Qinghai.tools.utils import Utils_
from Qinghai.tools.DB_mysql import *
from Qinghai.tools.re_time import Times
import datetime


class BjhdSpider(scrapy.Spider):
    name = 'bjhd'
    allowed_domains = ['bjhd.gov.cn']
    start_urls = ['http://bjhd.gov.cn/']

    def __init__(self, *args, **kwargs ):
        super(BjhdSpider, self).__init__()
        self.cates = [
            {"cate": "zbcg", "pages": 1},  # 招标采购
        ]
        self.t = Times()
        self.c_time = datetime.datetime.utcnow() - datetime.timedelta(days=2)

    def start_requests(self):
        url = "http://www.bjhd.gov.cn/zfcg/getnewsbypageindex?xwlbdm=zfcgys&pageIndex=mcilKnzDKt2L4e05w5kTHA%3D%3D&like="
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        list_url = re.findall('xwid":(\d+)', response.text)
        pub_times = re.findall('xwfbsj":(.*?),', response.text)
        # print(list_url,titles,pub_times)
        # print(name)
        # lists = ['295', '1086', '260', '99', '137', '1465', '510', '1806', '255', '343']
        item = {}
        # # 循环遍历
        for href, pub_time in zip(list_url, pub_times):
            # print(response.urljoin(href))
            item['link'] = 'http://www.bjhd.gov.cn/zfcg/ht/getdetailedinformation?xwlbmc=zfcgys&xwid='+href
            pub_time = re.findall('\\d{4}-\\d{2}-\\d{2}', pub_time)[0]
            PUBLISH = self.t.datetimes(pub_time)
            item['publish_time'] = PUBLISH.strftime('%Y-%m-%d')  # 发布时间
            print(item['publish_time'])
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
        item['title'] = response.xpath('//h1/text()').get().strip()
        item['uid'] = 'zf' + Utils_.md5_encrypt(item['title'] + item['link'] + item['publish_time'] )
        item['intro'] = ''
        item['abs'] = '1'
        item['content'] = response.text
        item['purchaser'] = ''
        item['create_time'] = str(datetime.datetime.now().strftime('%Y-%m-%d'))
        item['proxy'] = ''
        item['update_time'] = ''
        item['deleted'] = ''
        item['province'] = ''
        item['base'] = ''
        item['type'] = '采购公告'
        item['items'] = ''
        item['data_source'] = '00142'
        item['end_time'] = ''
        item['status'] = ''
        item['serial'] = ''

        yield item
