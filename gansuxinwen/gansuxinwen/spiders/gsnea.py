# -*- coding: utf-8 -*-

# @Time : 2022-07-13 15:33:49
# @Author : 石张毅
# @Site : http://www.gsnea.cn/page158?article_category=92
# @introduce: 甘肃新能源网

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


class GsneaSpider(scrapy.Spider):
    name = 'gsnea'
    def __init__(self, *args, **kwargs):
        super(GsneaSpider, self).__init__()
        self.cates = [
            {"cate": "newmain/right/zg", "pages": 1},  # 招6标公告
            {"cate": "newmain/jdpd/yj", "pages": 1},  # 招标公告
            {"cate": "ny/gdxw", "pages": 1},  # 招标公告
        ]
        self.t = Times()
        self.c_time = datetime.datetime.utcnow() - datetime.timedelta(days=2)

    def start_requests(self):

        url = f"http://www.gsnea.cn/page158?article_category=92"
        # print(url)
        yield scrapy.Request(url=url, callback=self.parse, dont_filter=True)

    def parse(self, response, *args):
        count_list = response.xpath("//*[contains(@class,'article_list-layer')]/ul/li")
        if count_list is []:
            return
        for count in count_list:
            item = GansuxinwenItem()
            # 列表页链接和发布时间
            item['link'] = response.urljoin(count.xpath(".//a/@href").get())
            item['title'] = count.xpath(".//a/@title").get()
            if item['title'] is None:
                continue
            day = count.xpath('.//span[1]/text()').get()
            month = count.xpath('.//span[2]/text()').get()
            pub_time = month+'-'+day
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
            item['province'] = '甘肃省'
            item['create_time'] = str(datetime.datetime.now().strftime('%Y-%m-%d'))
            item['data_source'] = '00676'
            item['status'] = ''
            item['base'] = ''
            yield scrapy.Request(item['link'], callback=self.parse_info, meta={'item': copy.deepcopy(item)},
                                 dont_filter=True)

    def parse_info(self, response):
        # print(response.text)
        if response.status != 200:
            return
        item = response.meta['item']
        item['author'] = '甘肃新能源网'
        # print(response.text)
        from lxml import etree
        html = etree.HTML(response.text)
        div_data = html.xpath('//*[@class="artview_content"]')
        item['content'] = etree.tostring(div_data[0], encoding='utf-8').decode()
        # print(item)
        yield item

