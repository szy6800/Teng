# -*- coding: utf-8 -*-

# @Author : 石张毅
# @Site :
# @introduce:

import scrapy
import scrapy
import copy
from Qinghai.tools.utils import Utils_
from Qinghai.tools.DB_mysql import *
from Qinghai.tools.re_time import Times
from lxml import etree
import datetime
import jsonpath
import json
import re

class GsTianshuiSpider(scrapy.Spider):
    name = 'gs_tianshui'
    def __init__(self, *args, **kwargs):
        super(GsTianshuiSpider, self).__init__()
        self.cates = [
          {"cate": "A01", "pages": 3,'types':'1'},  # 招标公告
          {"cate": "A01", "pages": 3,'types':'2'},  # 招标公告
          {"cate": "A99", "pages": 3,'types':'1'},  # 招标公告
          {"cate": "A99", "pages": 3,'types':'2'},  # 招标公告
          {"cate": "A02", "pages": 3,'types':'1'},  # 招标公告
          {"cate": "A02", "pages": 2,'types':'2'},  # 招标公告
          {"cate": "A03", "pages": 2,'types':'1'},  # 招标公告
          {"cate": "A03", "pages": 2,'types':'2'},  # 招标公告
          {"cate": "D", "pages": 2,'types':'1'},  # 招标公告
          {"cate": "D", "pages": 2,'types':'2'},  # 招标公告
          {"cate": "C", "pages": 2,'types':'1'},  # 招标公告
          {"cate": "C", "pages": 2,'types':'2'},  # 招标公告
        ]
        self.t = Times()
        self.c_time = datetime.datetime.utcnow() - datetime.timedelta(days=40)

    def start_requests(self):
        for each in self.cates:
            cate = each["cate"]
            pages = each["pages"]
            types = each["types"]
            for p in range(1, pages):
                # p = f"" if p else ""
                url = f"http://ggzyjy.tianshui.gov.cn/f/trade/annogoods/getAnnoItem?pageNo={p}&pageSize=20&prjpropertycode={cate}&annogoodstype={types}&type=&tabType=&isFrame=&annogoodsname="
                print(url)
                yield scrapy.Request(url=url, callback=self.parse)


    def parse(self, response, **kwargs):
        list_url = response.xpath('//*[@class="ejcotlist"]//ul/li//a/@href').getall()
        pub_times = response.xpath('//*[@class="ejcotlist"]//ul/li//a/following::span[1]/text()').getall()
        # print(titles)
        # 循环遍历
        for href, pub_time in zip(list_url, pub_times):
            item = dict()
            item['link'] = response.urljoin(href)
            # pub_time = re.findall('\\d{4}-\\d{2}-\\d{2}', pub_time)[0]
            PUBLISH = self.t.datetimes(pub_time)
            item['publish_time'] = PUBLISH.strftime('%Y-%m-%d')  # 发布时间
            ctime = self.t.datetimes(item['publish_time'])
            if ctime < self.c_time:
                print('文章发布时间大于规定时间，不予采集', item['link'])
                return
            # print(item['publish_time'],item['link'])
            yield scrapy.Request(item['link'], callback=self.parse_info, meta={'item': copy.deepcopy(item)},
                                 dont_filter=True)

    def parse_info(self, response):
        if response.status != 200:
            return
        item = response.meta['item']
        item['title'] = response.xpath("//*[contains(text(),'招标项目名称：')]/following::td[1]/text()|//*[@class='Protit']/text()|//*[@class='yAnnounceName']/text()").get()
        # 标题
        item['uuid'] = ''
        item['uid'] = 'zf' + Utils_.md5_encrypt(item['title'] + item['link'] + item['publish_time'])
        item['intro'] = ''
        item['abs'] = '1'
        # html = etree.HTML(response.text)
        # div_data = html.xpath('//*[@class="contLeft "]|//*[@class="contLeft"]')[0]
        item['content'] =response.xpath("string(//div[@class='jxTradingMainLeft'])").get().strip()
        # item['content'] =response.text

        item['purchaser'] = response.xpath("//*[contains(text(),'招标人：')]/following::td[1]/text()").get()
        item['create_time'] = str(datetime.datetime.now().strftime('%Y-%m-%d'))
        item['proxy'] = response.xpath("//*[contains(text(),'招标代理机构：')]/following::td[1]/text()").get()
        item['update_time'] = ''
        item['deleted'] = ''
        item['province'] = '甘肃省'
        item['base'] = ''
        item['type'] = '招标公告'
        item['items'] = response.xpath("//*[contains(text(),'项目类型：')]/following::td[1]/text()").get()
        item['data_source'] = '00402'
        item['end_time'] = ''
        item['status'] = ''
        item['serial'] = response.xpath("//*[contains(text(),'项目编号：')]/following::td[1]/text()").get()

        yield item