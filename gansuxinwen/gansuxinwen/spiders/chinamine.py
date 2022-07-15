# -*- coding: utf-8 -*-

# @Time : 2022-07-14 11:03:30
# @Author : 石张毅
# @Site :http://gs.chinamine-safety.gov.cn/web/toChannel.shtml?channelid=368871
# 2732269552&childerid=3688906045068456
# @introduce:  国家矿山安全监察局甘肃局


import re
import datetime
import json
import copy
from gansuxinwen.items import GansuxinwenItem
from gansuxinwen.tools.DB_mysql import *
from gansuxinwen.tools.re_time import Times
from gansuxinwen.tools.utils import Utils_
from gansuxinwen.tools.DB_redis import Redis_DB
import scrapy


class ChinamineSpider(scrapy.Spider):
    name = 'chinamine'
    def __init__(self, *args, **kwargs):
        super(ChinamineSpider, self).__init__()
        self.cates = [
            {"cate": "3688906045068456&parentid=3688906045068456", "pages": 2},  # 招6标公告
            {"cate": "3688924161826730&parentid=3688924161826730", "pages": 2},  # 招6标公告
            {"cate": "3688968856372054&parentid=3688968856372054", "pages": 2},  # 招6标公告
        ]
        self.t = Times()
        self.c_time = datetime.datetime.utcnow() - datetime.timedelta(days=2)

    def start_requests(self):
        for each in self.cates:
            cate = each["cate"]
            pages = each["pages"]
            for p in range(1, pages):
                # p = f"_{p}" if p else ""
                url = f"http://gs.chinamine-safety.gov.cn/web/tofindInfoList.shtml?channelid={cate}?page={p}"
                # print(url)
                yield scrapy.Request(url=url, callback=self.parse, dont_filter=True)

    def parse(self, response, *args):
        count_list = response.xpath('//*[@class="list-table"]/li')
        if count_list is []:
            return
        for count in count_list:
            item = GansuxinwenItem()
            # 列表页链接和发布时间
            item['link'] = response.urljoin(count.xpath("./a/@href").get())
            item['title'] = count.xpath("./a/@title").get()
            if item['title'] is None:
                continue
            pub_time = count.xpath('./span/text()').get()
            PUBLISH = self.t.datetimes(pub_time)
            item['publish_time'] = PUBLISH.strftime('%Y-%m-%d')  # 发布
            #print(item['publish_time'],item['link'],item['title'])
            ctime = self.t.datetimes(item['publish_time'])
            if ctime < self.c_time:
                print('文章发布时间大于规定时间，不予采集', item['link'])
                return
            item['uid'] = 'zf' + Utils_.md5_encrypt(item['title'] + item['link'] + item['publish_time'])
            if Redis_DB().Redis_pd(item['uid']) is True:  # 数据去重
                print(item['title'], '\033[0;35m <=======此数据已采集=======> \033[0m')
                return
            item['province'] = ''
            item['create_time'] = str(datetime.datetime.now().strftime('%Y-%m-%d'))
            item['data_source'] = '00679'
            item['status'] = ''
            item['base'] = ''
            yield scrapy.Request(item['link'], callback=self.parse_info, meta={'item': copy.deepcopy(item)},
                                 dont_filter=True)

    def parse_info(self, response):
        # print(response.text)
        if response.status != 200:
            return
        item = response.meta['item']

        item['author'] = '国家矿山安全监察局甘肃局'
        # print(response.text)
        # from lxml import etree
        # html = etree.HTML(response.text)
        # div_data = html.xpath('//*[@class="content"]')
        # item['content'] = etree.tostring(div_data[0], encoding='utf-8').decode()
        item['content'] = response.text
        # print(item)
        yield item

