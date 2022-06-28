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
    # start_urls = ['http://www.bjhd.gov.cn/zfcg/getnewsbypageindex?xwl_{}'.format(i) for i in range(1,10) ]

    def __init__(self, *args, **kwargs ):
        super(BjhdSpider, self).__init__()
        self.t = Times()
        self.c_time = datetime.datetime.utcnow() - datetime.timedelta(days=8)

    def start_requests(self):
        url = f"http://www.bjhd.gov.cn/ggzyjy/zfcgQb/index.html"
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        list_url = response.xpath('//*[@class="article-info"]/a/@href').getall()
        pub_times = response.xpath('//*[@class="release-time"]/text()').getall()
        # # 循环遍历
        for href, pub_time in zip(list_url, pub_times):
            item = {}
            # print(response.urljoin(href))
            item['link'] =response.urljoin(href)
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
        item['title'] = response.xpath('//*[@class="detail-title"]/text()').get().strip()
        item['uid'] = 'zf' + Utils_.md5_encrypt(item['title'] + item['link'] + item['publish_time'] )
        item['intro'] = ''
        item['abs'] = '1'
        from lxml import etree
        html = etree.HTML(response.text)
        div_data = html.xpath('//*[@class="content2"]')
        item['content'] = etree.tostring(div_data[0], encoding='utf-8').decode()
        item['purchaser'] = ''
        item['create_time'] = str(datetime.datetime.now().strftime('%Y-%m-%d'))
        item['proxy'] = ''
        item['update_time'] = ''
        from Qinghai.tools.uredis import Redis_DB
        if Redis_DB().Redis_pd(item['uid']) is True:  #数据去重
            print(item['uid'], '\033[0;35m <=======此数据已采集=======> \033[0m')
            return
        item['deleted'] = ''
        item['province'] = '北京市'
        item['base'] = ''
        item['type'] = response.xpath('//*[@id="chinner1"]/a[last()]/text()').get()
        item['items'] = ''
        item['data_source'] = '00142'
        item['end_time'] = ''
        item['status'] = ''
        item['serial'] = ''

        yield item
