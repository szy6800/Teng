# -*- coding: utf-8 -*-

# @Author : 石张毅
# @Site :安徽建工集团 http://cp.aceg.com.cn/


import scrapy
import scrapy
import copy
from Qinghai.tools.utils import Utils_
from Qinghai.tools.DB_mysql import *
from Qinghai.tools.re_time import Times
import datetime
import re


class EcegSpider(scrapy.Spider):
    name = 'eceg'
    # allowed_domains = ['eceg.cn']
    # start_urls = ['http://eceg.cn/']

    def __init__(self, *args, **kwargs ):
        super(EcegSpider, self).__init__()
        self.cates = [
            {"cate": "1", "pages": 2},  # 招标公告
            {"cate": "11", "pages": 3},  # 补疑澄清
            {"cate": "12", "pages": 3},  # 中标公示
            {"cate": "10", "pages": 3},  # 流标公告

        ]
        self.t = Times()
        self.c_time = datetime.datetime.utcnow() - datetime.timedelta(days=3)

    def start_requests(self):
        for each in self.cates:
            cate = each["cate"]
            pages = each["pages"]
            for p in range(1,pages):
                url = f"http://cp.aceg.com.cn/webportal/index/bidnotice/list/1.do?cate={cate}&pn={p}"
                yield scrapy.Request(url=url, callback=self.parse,dont_filter=True)

    def parse(self, response):
        # print(response.text)
        item = {}
        # 列表页链接和发布时间
        list_url = response.xpath('//*[@class="noticelist"]/ul/li//a/@href').getall()
        titles = response.xpath('//*[@class="noticelist"]/ul/li//a/text()[3]').getall()
        pub_times = response.xpath('//*[@class="noticelist"]/ul/li//a/following::span[1]/text()').getall()
        # print(titles)
        # 循环遍历
        for href, title, pub_time in zip(list_url,titles, pub_times):
            href = href.replace('show','content')
            item['link'] = response.urljoin(href)
            item['title'] = title.strip()
            if item['title'] is None:
                continue
            pub_time = re.findall('\\d{4}-\\d{2}-\\d{2}', pub_time)[0]
            PUBLISH = self.t.datetimes(pub_time)
            item['publish_time'] = PUBLISH.strftime('%Y-%m-%d')  # 发布时间
            ctime = self.t.datetimes(item['publish_time'])
            if ctime < self.c_time:
                print('文章发布时间大于规定时间，不予采集', item['link'])
                return
            # print(item['link'], item['publish_time'])
            yield scrapy.Request(item['link'], callback=self.parse_info, meta={'item': copy.deepcopy(item)},dont_filter=True)

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
        div_data = html.xpath('//*[@id="content"]')
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
        item['province'] = '安徽省'
        item['base'] = ''
        item['type'] = '招标采购'
        item['items'] = ''
        item['data_source'] = '00123'
        item['end_time'] = ''
        item['status'] = ''
        item['serial'] = ''

        yield item

