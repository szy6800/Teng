# -*- coding: utf-8 -*-

# @Time : 2022-07-14 15:03:58
# @Author : 石张毅
# @Site : http://www.ce.cn/cysc/jtys/yw/index.shtml
# http://www.ce.cn/cysc/jtys/tielu/index.shtml
# http://www.ce.cn/cysc/jtys/hangkong/index.shtml
# http://www.ce.cn/cysc/jtys/gonglu/index.shtml
# http://www.ce.cn/cysc/jtys/haiyun/index.shtml
# http://www.ce.cn/cysc/jtys/csjt/index.shtml
# http://www.ce.cn/cysc/jtys/zhwl/index.shtml
# @introduce: 中国经济网-交通频道

import scrapy
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

class Ce1Spider(scrapy.Spider):
    name = 'ce1'

    def __init__(self, *args, **kwargs):
        super(Ce1Spider, self).__init__()
        self.cates = [
            {"cate": "jtys/yw", "pages": 1},  # 招6标公告
            {"cate": "jtys/tielu", "pages": 1},  # 招标公告
            {"cate": "jtys/hangkong/", "pages": 1},  # 招标公告
            {"cate": "jtys/gonglu", "pages": 1},  # 招标公告
            {"cate": "jtys/csjt", "pages": 1},  # 招标公告
            {"cate": "jtys/zhwl", "pages": 1},  # 招标公告
        ]
        self.t = Times()
        self.c_time = datetime.datetime.utcnow() - datetime.timedelta(days=2)

    def start_requests(self):
        for each in self.cates:
            cate = each["cate"]
            pages = each["pages"]
            for p in range(0, pages):
                p = f"_{p}" if p else ""
                url = f"http://www.ce.cn/cysc/{cate}/index{p}.shtml"
                # print(url)
                yield scrapy.Request(url=url, callback=self.parse, dont_filter=True)

    def parse(self, response, *args):
        count_list = response.xpath('//*[@class="left"]/ul/li')
        if count_list is []:
            return
        for count in count_list:
            item = GansuxinwenItem()
            # 列表页链接和发布时间
            item['link'] = response.urljoin(count.xpath("./a/@href").get())
            item['title'] = count.xpath("./a/text()").get()
            if item['title'] is None:
                continue
            pub_time = count.xpath('./text()[2]').get()
            pub_time = re.findall('\d{4}/\d{2}/\d{2}', pub_time)[0]
            PUBLISH = self.t.datetimes(pub_time)
            item['publish_time'] = PUBLISH.strftime('%Y-%m-%d')  # 发布
            # print(item['publish_time'],item['link'],item['title'])
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
            item['data_source'] = '00681'
            item['status'] = ''
            item['base'] = ''
            yield scrapy.Request(item['link'], callback=self.parse_info, meta={'item': copy.deepcopy(item)},
                                 dont_filter=True)

    def parse_info(self, response):
        # print(response.text)
        if response.status != 200:
            return
        item = response.meta['item']
        try:
            author = re.findall('来源[:： \n]+(.*?)<', response.text)[0]
            item['author'] = author
        except:
            item['author'] = '中国经济网'
        # print(response.text)
        from lxml import etree
        html = etree.HTML(response.text)
        div_data = html.xpath('//*[@class="content"]')
        item['content'] = etree.tostring(div_data[0], encoding='utf-8').decode()
        # print(item)
        yield item

