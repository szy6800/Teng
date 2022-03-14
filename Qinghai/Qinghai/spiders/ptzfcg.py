# -*- coding: utf-8 -*-

# @Author : 石张毅
# @Site :http://www.ptzfcg.gov.cn  福建省政府采购网
# @introduce: 政府采购信息公开

import scrapy
import copy
from Qinghai.tools.utils import Utils_
from Qinghai.tools.DB_mysql import *
from Qinghai.tools.re_time import Times
import datetime


class PtzfcgSpider(scrapy.Spider):
    name = 'ptzfcg'
    allowed_domains = ['ptzfcg.gov.cn']
    start_urls = ['http://ptzfcg.gov.cn/']

    def __init__(self, *args, **kwargs ):
        super(PtzfcgSpider, self).__init__()
        self.cates = [
            {"cate": "zbgg", "pages": 20},  # 招标公告


        ]
        self.t = Times()
        self.c_time = datetime.datetime.utcnow() - datetime.timedelta(days=4)

    def start_requests(self):
        for each in self.cates:
            cate = each["cate"]
            pages = each["pages"]
            for p in range(1, pages):
                # p = f"_{p+1}" if p else ""
                url = f"http://www.ptzfcg.gov.cn/350300/noticelist/d03180adb4de41acbb063875889f9af1/?page={p}"
                yield scrapy.Request(url=url, callback=self.parse,dont_filter=True)

    def parse(self, response):
        # print(response.text)
        item = {}
        # 列表页链接和发布时间
        list_url = response.xpath('//*[@class="wrapTable"]//a/@href').getall()
        # print(list_url)
        titles = response.xpath('//*[@class="wrapTable"]//a/text()').getall()
        # print(titles)
        pub_times = response.xpath('//*[@class="wrapTable"]//a/following::td[1]/text()').getall()
        #采购方
        purchasers = response.xpath('//*[@class="gradeX"]/td[3]/text()').getall()
        #循环遍历
        for href, title, pub_time, purchaser in zip(list_url, titles, pub_times, purchasers):
            # print(response.urljoin(href))
            item['link'] = response.urljoin(href.strip())
            # 购买方
            item['purchaser'] = purchaser.strip()
            item['title'] = title.strip()
            if item['title'] is None:
                continue
            # pub_time = re.findall('\\d{4}-\\d{2}-\\d{2}', pub_time)[0]
            PUBLISH = self.t.datetimes(pub_time)
            item['publish_time'] = PUBLISH.strftime('%Y-%m-%d')  # 发布时间
            # print(item['publish_time'])
            ctime = self.t.datetimes(item['publish_time'])
            if ctime < self.c_time:
                print('文章发布时间大于规定时间，不予采集', item['link'])
                return
            # print(item['link'], item['publish_time'],item['title'],item['purchaser'])
            yield scrapy.Request(item['link'], callback=self.parse_info, meta={'item': copy.deepcopy(item)},dont_filter=True)

    def parse_info(self, response):
        if response.status != 200:
            return
        item = response.meta['item']
        # 标题
        item['uuid'] = ''
        item['uid'] = 'zf' + Utils_.md5_encrypt(item['title'] + item['link'])
        item['intro'] = ''
        item['abs'] = ''
        item['content'] = response.text
        item['create_time'] = str(datetime.datetime.now().strftime('%Y-%m-%d'))
        item['proxy'] = ''
        item['update_time'] = ''
        item['deleted'] = ''
        item['province'] = '福建省'
        item['base'] = ''
        item['type'] = '政府采购信息公开 '
        item['items'] = ''
        item['data_source'] = '00149'
        item['end_time'] = ''
        item['status'] = ''
        item['serial'] = ''

        yield item
