# -*- coding: utf-8 -*-

# @Author : 石张毅
# @Site :必联网  http://www.ebnew.com
# @introduce: 国际招标和国内招标
import re
from lxml import etree

import scrapy
import copy
from Qinghai.tools.utils import Utils_
from Qinghai.tools.DB_mysql import *
from Qinghai.tools.re_time import Times
import datetime
import jsonpath
import json



class EbnewSpider(scrapy.Spider):
    name = 'ebnew'
    allowed_domains = ['ebnew.com']
    start_urls = ['http://ebnew.com/']

    def __init__(self, *args, **kwargs ):
        super(EbnewSpider, self).__init__()
        # self.cates = [
        #
        #     {"cate": "000", "pages": 2},  # 招标公告
        #     # {"cate": "001", "pages": 1},  # 变更公告
        #     # {"cate": "002", "pages": 1},  # 候选人公示
        #     # {"cate": "003", "pages": 1},  # 中标\流标公告
        #
        # ]
        self.t = Times()
        self.c_time = datetime.datetime.utcnow() - datetime.timedelta(days=5)

    def start_requests(self):
        url = "https://ss.ebnew.com/tradingSearch/index.htm"
        for i in range(1, 100):
            formdata = {
                "infoClassCodes": "",
                "rangeType": "",
                "projectType": "bid",
                "fundSourceCodes": "",
                "dateType": "",
                "startDateCode": "",
                "endDateCode": "",
                "normIndustry": "",
                "normIndustryName": "",
                "zone": "",
                "zoneName": "",
                "zoneText": "",
                "key": "",
                "pubDateType": "",
                "pubDateBegin": "",
                "pubDateEnd": "",
                "sortMethod": "timeDesc",
                "orgName": "",
                "currentPage": "{}".format(i),
            }
            yield scrapy.FormRequest(url=url, formdata=formdata, callback=self.parse, dont_filter=True)

    def parse(self, response, **kwargs):
        # print(response.text)
        item = {}
        list_url = response.xpath("//*[contains(@href,'.com/businessShow/')]/@href").getall()
        titles = response.xpath("//*[contains(@href,'.com/businessShow/')]/@title").getall()
        pub_times = response.xpath("//*[contains(@href,'.com/businessShow/')]/following::i[1]/text()").getall()
        # print(pub_times)
        # print(titles,pub_times)
        # 循环遍历
        for href, title, pub_time in zip(list_url, titles, pub_times):

            # print(response.urljoin(href))
            item['link'] = response.urljoin(href)
            item['title'] = title.strip()
            if item['title'] is None:
                continue
            pub_time = re.findall('\d{4}-\d{2}-\d{2}', pub_time.strip())[0]
            # print(pub_time)
            PUBLISH = self.t.datetimes(pub_time.strip())
            item['publish_time'] = PUBLISH.strftime('%Y-%m-%d')  # 发布时间
            # # print(item['publish_time'])
            ctime = self.t.datetimes(item['publish_time'])
            if ctime < self.c_time:
                print('文章发布时间大于规定时间，不予采集', item['link'])
                return
            # print(item['link'], item['publish_time'],item['title'])
            yield scrapy.Request(item['link'], callback=self.parse_info, meta={'item': copy.deepcopy(item)},
                                 dont_filter=True)

    def parse_info(self, response):
        if response.status != 200:
            return
        item = response.meta['item']
        # 标题
        item['uuid'] = ''
        item['uid'] = 'zf' + Utils_.md5_encrypt(item['title'] + item['link'] + item['publish_time'] )
        item['intro'] = ''
        item['abs'] = '1'
        html = etree.HTML(response.text)
        div_data = html.xpath('//*[@id="notLogin"]')
        item['content'] = etree.tostring(div_data[0], encoding='utf-8').decode()
        item['purchaser'] = ''
        item['create_time'] = str(datetime.datetime.now().strftime('%Y-%m-%d'))
        item['proxy'] = ''
        item['update_time'] = ''
        item['deleted'] = ''
        province = response.xpath("//span[contains(text(),'招标地区：')]/following-sibling::span[1]/text()").get()
        if province is None:
            item['province'] = ''
        else:
            item['province'] = province
        item['base'] = ''
        item['type'] = response.xpath("//span[contains(text(),'公告类型：')]/following-sibling::span[1]/text()").get().strip()
        item['items'] = response.xpath("//span[contains(text(),'所属行业：')]/following-sibling::span[1]/text()").get().replace(';','')
        item['data_source'] = '00135'
        item['status'] = ''
        end_time = response.xpath("//span[contains(text(),'截止时间：')]/following-sibling::span[1]/text()").get()
        if end_time is None:
            item['end_time'] = ''
        else:
            end_time = self.t.datetimes(end_time)
            item['end_time'] = end_time.strftime('%Y-%m-%d')  # 发布时间
        item['serial'] = ''
        yield item

