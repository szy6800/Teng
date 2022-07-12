# -*- coding: utf-8 -*-

# @Time : 2022-07-12 11:36:04
# @Author : 石张毅
# @Site : https://www.china-aii.com/news?pn=2&ty=2
# @introduce:中国工业互联网研究院
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


class ChinaAiiSpider(scrapy.Spider):
    name = 'china_aii'
    def __init__(self, *args, **kwargs):
        super(ChinaAiiSpider, self).__init__()
        self.L = {
        }
        self.t = Times()
        self.c_time = datetime.datetime.utcnow() - datetime.timedelta(days=2)

    def start_requests(self):
        for p in range(1,2):
            new_url = f'https://www.china-aii.com/api/news/show/newsList?pageNum={p}&' \
                      f'pageSize=6&typeId=3260774339377122566'
            yield scrapy.Request(new_url, callback=self.parse)

    def parse(self, response, *args):
        json_text = json.loads(response.text)
        count_list = json_text['data']['rows']
        for count in count_list:
            item = GansuxinwenItem()
            ids = count['id']
            item['link'] = f'https://www.china-aii.com/api/news/show/newsDetails?newsId={ids}'
            item['title'] = count['title']
            if item['title'] is None:
                continue
            pub_time = count['publishDate']
            PUBLISH = self.t.datetimes(pub_time)
            item['publish_time'] = PUBLISH.strftime('%Y-%m-%d')  # 发布
            # print(item['link'],item['title'],item['publish_time'])
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
            item['data_source'] = '00670'
            item['status'] = ''
            item['base'] = ''
            yield scrapy.Request(item['link'], callback=self.parse_info, meta={'item': copy.deepcopy(item)},
                                 dont_filter=True)

    def parse_info(self, response):
        if response.status != 200:
            return
        item = response.meta['item']
        json_text = json.loads(response.text)
        count_list = json_text['data']
        item['author'] = count_list['showPublishName']
        item['content'] = count_list['content']
        yield item

