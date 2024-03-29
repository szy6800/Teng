# -*- coding: utf-8 -*-

# @Author : 石张毅
# @Site :http://www.xndyyljt.com/?p=83 西宁市第一人名医院
# @introduce: 招标公告 中标公示

import scrapy
import scrapy
import copy
from Qinghai.tools.utils import Utils_
from Qinghai.tools.DB_mysql import *
from Qinghai.tools.re_time import Times
import datetime
from Qinghai.tools.uredis import Redis_DB

class XndyyljtSpider(scrapy.Spider):
    name = 'xndyyljt'
    allowed_domains = ['xndyyljt.com']
    start_urls = ['http://xndyyljt.com/']

    def __init__(self, *args, **kwargs ):
        super(XndyyljtSpider, self).__init__()
        self.cates = [
            {"cate": "83", "pages": 2},  # 招标公告
            {"cate": "84", "pages": 2},  # 中标公示

        ]
        self.t = Times()
        self.c_time = datetime.datetime.utcnow() - datetime.timedelta(days=4)

    def start_requests(self):
        for each in self.cates:
            cate = each["cate"]
            pages = each["pages"]
            for p in range(1, pages):
                # p = f"_{p+1}" if p else ""
                url = f"http://www.xndyyljt.com/?p={cate}&mdtp={p}.html"
                yield scrapy.Request(url=url, callback=self.parse,dont_filter=True)

    def parse(self, response):
        # print(response.text)
        item = {}
        # 列表页链接和发布时间
        list_url = response.xpath('//*[@id="newlist"]/ul/li/a/@href').getall()
        # print(list_url)
        titles = response.xpath('//*[@id="newlist"]/ul/li/a/text()').getall()
        # print(titles)
        pub_times = response.xpath('//*[@id="newlist"]/ul/li/a/preceding::span[1]/text()').getall()
        if "p=83" in response.url:
            item['type'] = "招标公告"
        if "p=84" in response.url:
            item['type'] = "中标公示"
        #循环遍历
        for href, title, pub_time in zip(list_url, titles, pub_times):
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

        item['intro'] = ''
        item['abs'] = '1'
        from lxml import etree
        html = etree.HTML(response.text)
        div_data = html.xpath('//*[@id="newcontent"]')
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

        # 行业
        item['items'] = ''
        # 类型编号
        item['data_source'] = '00169'
        item['end_time'] = ''
        item['status'] = ''
        # 采购编号
        item['serial'] = ''

        yield item