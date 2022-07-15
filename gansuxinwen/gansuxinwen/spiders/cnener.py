# -*- coding: utf-8 -*-

# @Time : 2022-07-13 13:45:40
# @Author : 石张毅
# @Site : http://www.cnenergynews.cn/guonei/list_80_1.html
# @introduce:中国能源报社官网
import re
import calendar
import datetime
import json
import copy
import time
from gansuxinwen.items import GansuxinwenItem
from gansuxinwen.tools.DB_mysql import *
from gansuxinwen.tools.re_time import Times
from gansuxinwen.tools.utils import Utils_
from gansuxinwen.tools.DB_redis import Redis_DB
import scrapy


def get_daylis(year, month):
    """
    获取当月日期列表
    parameter:
        month 202011
    return:
        [20201101,...,20201130]
    """
    day_lis = []
    for day in range(1, calendar.monthrange(year, month)[1] + 1):
        # 补0的用法
        day_lis.append('{}{:0>2d}{:0>2d}'.format(year,month,day))
        # day_lis.append('%s%s%s' % (year, '-%02d-' % month, '%02d' % (day)))
    return day_lis


class CnenergynewsSpider(scrapy.Spider):

    name = 'cnenergynews'

    def __init__(self, *args, **kwargs):
        super(CnenergynewsSpider, self).__init__()
        self.cates = [
            # {"cate": "macroeconomy", "pages": 2},  # 招标公告

        ]
        self.t = Times()
        # 2022年7月
        # self.dates = get_daylis(2022,7)
        self.c_time = datetime.datetime.utcnow() - datetime.timedelta(days=2)

    def start_requests(self):
        # p = f"_{p + 1}" if p else ""
        f = time.strftime('%Y%m%d', time.localtime())
        url = f"http://www.cnenergynews.cn/js/80/mi4_sub_articles_{f}.js?v=20220713104812"
        # print(url)
        yield scrapy.Request(url=url, callback=self.parse, dont_filter=True)

    def parse(self, response, *args):
        res = re.findall('\[.*?\]',response.text)[0]
        json_text = json.loads(res)
        # print(json_text)
        for count in json_text:
            item = GansuxinwenItem()
            item['link'] = count['url']
            item['title'] = count['title']
            if item['title'] is None:
                continue
            pub_time = count['pub_date']
            pub_time = re.findall('\d{4}-\d{2}-\d{2}', pub_time)[0]
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
            item['data_source'] = '00675'
            item['status'] = ''
            item['base'] = ''
            yield scrapy.Request(item['link'], callback=self.parse_info, meta={'item': copy.deepcopy(item)},
                                 dont_filter=True)

    def parse_info(self, response):
        if response.status != 200:
            return
        item = response.meta['item']
        item['author'] = response.xpath('//*[@class="title-icon-item item-a"]/text()').get()
        # print(response.text)
        from lxml import etree
        html = etree.HTML(response.text)
        div_data = html.xpath('//*[@class="article-content"]')
        item['content'] = etree.tostring(div_data[0], encoding='utf-8').decode()
        # print(item)
        yield item
