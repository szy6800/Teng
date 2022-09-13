# -*- coding: utf-8 -*-

# @Time : 2022-08-29 15:16:11
# @Author : 石张毅
# @Site : http://61.178.200.57:8003/bidder/announcement/lookAnnouncementInfoPage?annId=36633&annKind=2
# @introduce: annId=36666 自增 100左右
import re

import scrapy
import copy
from Qinghai.tools.utils import Utils_
from Qinghai.tools.DB_mysql import *
from Qinghai.tools.re_time import Times
from lxml import etree
import datetime
from Qinghai.tools.uredis import Redis_DB


class GsBuiSpider(scrapy.Spider):
    name = 'gs_bui'

    def __init__(self, *args, **kwargs):
        super(GsBuiSpider, self).__init__()
        self.t = Times()
        self.c_time = datetime.datetime.utcnow() - datetime.timedelta(days=7)

    def start_requests(self):
        for i in range(37500,37900):
            url = 'http://61.178.200.57:8003/bidder/announcement/lookAnnouncementInfoPage?annId={}&annKind=2'.format(i)
            yield scrapy.Request(url=url, callback=self.parse, dont_filter=True)
    #
    def parse(self, response, *args, **kwargs):
        item = dict()
        # 列表页链接和发布时间
        item['link'] = response.url
        item['title'] = response.xpath('//*[@class="title"]/text()').get()
        item['type'] = ''
        pub_time = response.xpath("//div[@class='check']//*[contains(text(),'公告开始时间')]/following::input[1]/@value|//div[@class='check']//*[contains(text(),'公示开始时间')]/following::input[1]/@value").get()
        PUBLISH = self.t.datetimes(pub_time)
        item['publish_time'] = PUBLISH.strftime('%Y-%m-%d')  # 发布时间
        # print(item['publish_time'],item['link'],item['title'])
        item['uid'] = 'zf' + Utils_.md5_encrypt(item['title'] + item['link'] + item['publish_time'])
        ctime = self.t.datetimes(item['publish_time'])
        if ctime < self.c_time:
            print('文章发布时间大于规定时间，不予采集', item['link'])
            return
        # if Redis_DB().Redis_pd(item['uid']) is True:  # 数据去重
        #     print(item['uid'], '\033[0;35m <=======此数据已采集=======> \033[0m')
        #     return
        item['uuid'] = ''
        item['intro'] = ''
        item['abs'] = '1'
        item['content'] = re.findall("ue1.setContent\('(.*?)'\);", response.text)[0]
        item['purchaser'] = response.xpath("//div[@class='check']//*[contains(text(),'招标人')]/following::input[1]/@value").get()
        item['create_time'] = str(datetime.datetime.now().strftime('%Y-%m-%d'))
        item['proxy'] = ''
        item['update_time'] = ''
        item['deleted'] = ''
        item['province'] = '甘肃省'
        item['base'] = ''
        item['items'] = ''
        item['data_source'] = '00767'
        item['end_time'] = ''
        item['status'] = ''
        item['serial'] = ''
        # print(item)
        #
        yield item


