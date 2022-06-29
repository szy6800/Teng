# -*- coding: utf-8 -*-

# @Author : 石张毅
# @Site : http://www.qysggzyjy.cn/f/newtrade/tenderannquainqueryanns/list?selectedProjectType=1&idxType=A01&way=undefined&nature=1&typetab=0
# @introduce:庆阳市公共资源交易中心

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


class GsQysggzyjySpider(scrapy.Spider):
    name = 'gs_qysggzyjy'
    def __init__(self, *args, **kwargs):
        super(GsQysggzyjySpider, self).__init__()
        self.cates = [
            {"cate": "newtrade/tenderannquainqueryanns/getListByProjectTypePage?projectType=A&purchaseCode=&gsPlatformNavActive=1&projectName=&tradePlatformId=1&tenderMode=all&pageNo=", "pages": 3},  # 招标公告
            {"cate": "newtrade/tenderannquainqueryanns/getListByProjectTypePage?projectType=B&purchaseCode=&gsPlatformNavActive=1&projectName=&tradePlatformId=1&tenderMode=all&pageNo=", "pages": 3},  # 招标公告
            {"cate": "newtrade/tenderannquainqueryanns/getListByProjectTypePage?projectType=C&purchaseCode=&gsPlatformNavActive=1&projectName=&tradePlatformId=1&tenderMode=all&pageNo=", "pages": 3},  # 招标公告
            {"cate": "newtrade/tenderannquainqueryanns/getListByProjectTypePage?projectType=D&purchaseCode=&gsPlatformNavActive=1&projectName=&tradePlatformId=1&tenderMode=all&pageNo=", "pages": 3},  # 招标公告
            {"cate": "newtrade/tenderannquainqueryanns/getImportantList?type=&noticename=&pageNo=", "pages": 3},  # 招标公告
          #  {"cate": "purchase/purchaseAnnoment/getAnnoList?type=sunAll&tabType=1&tradePlatformId=1&noticename=&pageNo=", "pages": 2},  # 招标公告
        ]
        self.t = Times()
        self.c_time = datetime.datetime.utcnow() - datetime.timedelta(days=7)

    def start_requests(self):
        for each in self.cates:
            cate = each["cate"]
            pages = each["pages"]
            for p in range(1, pages):
                # p = f"" if p else ""
                url = f"http://www.qysggzyjy.cn/f/{cate}{p}"
                yield scrapy.Request(url=url, callback=self.parse)


    def parse(self, response, **kwargs):
        list_url = response.xpath('//a[@class="gsPropertyBox"]/@href | //ul/a/@href').getall()
        pub_times = response.xpath('//span[@class="time_index"]/text()').getall()
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
        item['content'] =response.xpath("string(//div[@class='contLeft'])").get().strip()
        # item['content'] =response.text

        item['purchaser'] = response.xpath("//*[contains(text(),'招标人/采购人：')]/following::td[1]/text()").get()
        item['create_time'] = str(datetime.datetime.now().strftime('%Y-%m-%d'))
        item['proxy'] = response.xpath("//*[contains(text(),'招标代理机构：')]/following::td[1]/text()").get()
        item['update_time'] = ''
        from Qinghai.tools.uredis import Redis_DB
        if Redis_DB().Redis_pd(item['uid']) is True:  #数据去重
            print(item['uid'], '\033[0;35m <=======此数据已采集=======> \033[0m')
            return
        item['deleted'] = ''
        item['province'] = '甘肃省'
        item['base'] = ''
        item['type'] = '招标公告'
        item['items'] = response.xpath("//*[contains(text(),'项目类型：')]/following::td[1]/text()").get()
        item['data_source'] = '00401'
        item['end_time'] = ''
        item['status'] = ''
        item['serial'] = response.xpath("//*[contains(text(),'项目编号：')]/following::td[1]/text()").get()

        yield item
