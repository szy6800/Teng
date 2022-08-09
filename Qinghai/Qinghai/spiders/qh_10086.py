# -*- coding: utf-8 -*-

# @Time : 2022-08-08 14:43:13
# @Author : 石张毅
# @Site :  https://b2b.10086.cn/b2b/main/showBiao!preShowBiao.html?noticeType=list1#this
# @introduce: 中国移动


import re
import copy
from Qinghai.tools.utils import Utils_
from Qinghai.tools.DB_mysql import *
from Qinghai.tools.re_time import Times
import datetime
from Qinghai.tools.uredis import Redis_DB
import scrapy

import scrapy


class Qh10086Spider(scrapy.Spider):
    name = 'qh_10086'

    custom_settings = {
        'DEFAULT_REQUEST_HEADERS': {
            "Referer": "https://b2b.10086.cn/b2b/main/showBiao!preShowBiao.html?noticeType=list1",
        }
    }

    def __init__(self, *args, **kwargs):
        super(Qh10086Spider, self).__init__()
        self.cates = [
            {"cate": "1698", "pages": 2},
        ]
        self.t = Times()
        self.c_time = datetime.datetime.utcnow() - datetime.timedelta(days=3)

    def start_requests(self):
        url = 'https://b2b.10086.cn/b2b/main/showBiao!showZhaobiaoResult.html'
        for i in range(1,4):
            data = {
                "page.currentPage": "{}".format(i),
                "page.perPageSize": "20",
                "noticeBean.companyName": "",
                "noticeBean.title": "",
                "noticeBean.startDate": "",
                "noticeBean.endDate": "",
            }
            yield scrapy.FormRequest(url=url, formdata=data,callback=self.parse, dont_filter=True)


    def parse(self, response, **kwargs):
        # print(response.text)
        # 列表页链接和发布时间
        count_list = response.xpath('//*[@class="jtgs_table"]//tr[position()>1]')
        if count_list is []:
            return
        for count in count_list:
            item = dict()
            # 列表页链接和发布时间
            link =count.xpath('./@onclick').get()
            res = re.findall("\d{6}", link)[0]
            item['link'] = 'https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id='+res
            item['title'] = count.xpath('./td[2]/a/text()').get()
            if item['title'] is None:
                continue
            item['type'] = '招标采购公告'
            item['purchaser'] = count.xpath('./td[1]/text()').get()
            item['items'] = ''
            pub_time = count.xpath('./td[3]/text()').get()
            PUBLISH = self.t.datetimes(pub_time)
            item['publish_time'] = PUBLISH.strftime('%Y-%m-%d')  # 发布时间
            #print(item['publish_time'],item['link'],item['title'],item['purchaser'])
            item['uid'] = 'zf' + Utils_.md5_encrypt(item['title'] + item['link'] + item['publish_time'])
            ctime = self.t.datetimes(item['publish_time'])
            if ctime < self.c_time:
                print('文章发布时间大于规定时间，不予采集', item['link'])
                return
            if Redis_DB().Redis_pd(item['uid']) is True:  # 数据去重
                print(item['uid'], '\033[0;35m <=======此数据已采集=======> \033[0m')
                return
            yield scrapy.Request(item['link'], callback=self.parse_info, meta={'item': copy.deepcopy(item)},
                                 dont_filter=True)

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
        div_data = html.xpath('//*[@id="mobanDiv"]')
        item['content'] = etree.tostring(div_data[0], encoding='utf-8').decode()
        item['create_time'] = str(datetime.datetime.now().strftime('%Y-%m-%d'))
        item['proxy'] = ''
        item['update_time'] = ''
        item['deleted'] = ''
        item['province'] = ''
        item['base'] = ''
        item['data_source'] = '00721'
        item['end_time'] = ''
        item['status'] = ''
        item['serial'] = ''
        # print(item)
        yield item

