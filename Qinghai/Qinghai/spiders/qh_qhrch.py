# -*- coding: utf-8 -*-

# @Time : 2022-07-29 13:59:54
# @Author : 石张毅
# @Site :https://www.qhrch.com/index.php/zbgg.html
# https://www.qhrch.com/index.php/cgyxgs.html
# https://www.qhrch.com/index.php/zbgs.html
# https://www.qhrch.com/index.php/zybecgg.html
# https://www.qhrch.com/index.php/ggbg.html
# @introduce: 青海红十字医院

import re
import copy
from Qinghai.tools.utils import Utils_
from Qinghai.tools.DB_mysql import *
from Qinghai.tools.re_time import Times
import datetime
from Qinghai.tools.uredis import Redis_DB
import scrapy



class QhQhrchSpider(scrapy.Spider):
    name = 'qh_qhrch'

    def __init__(self, *args, **kwargs):
        super(QhQhrchSpider, self).__init__()
        self.cates = [
            {"cate": "zbgg", "pages": 2},
            {"cate": "cgyxgs", "pages": 2},
            {"cate": "zbgs", "pages": 2},
            {"cate": "zybecgg", "pages": 2},
            {"cate": "ggbg", "pages": 2},
        ]
        self.t = Times()
        self.c_time = datetime.datetime.utcnow() - datetime.timedelta(days=3)

    def start_requests(self):
        for each in self.cates:
            cate = each["cate"]
            url = f"https://www.qhrch.com/index.php/{cate}.html"
            # print(url)
            yield scrapy.Request(url=url, callback=self.parse, dont_filter=True)

    def parse(self, response, **kwargs):
        # 列表页链接和发布时间
        count_list = response.xpath('//*[@class="textlist"]/li')
        types = response.xpath('//*[@id="location"]/a[last()]/text()').get()
        if count_list is []:
            return
        for count in count_list:
            item = dict()
            # 列表页链接和发布时间
            item['link'] = response.urljoin(count.xpath('./a/@href').get())
            item['title'] = count.xpath('./a/@title').get()
            if item['title'] is None:
                continue
            item['type'] = types
            # pub_time = re.findall('\d{4}/\d{2}/\d{2}', response.text)[0].replace('/', '-')
            pub_time = count.xpath('./span/text()').get()
            PUBLISH = self.t.datetimes(pub_time)
            item['publish_time'] = PUBLISH.strftime('%Y-%m-%d')  # 发布时间
            # print(item['publish_time'],item['link'],item['title'],item['type'])
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
        div_data = html.xpath('//*[@class="InfoContent"]')
        item['content'] = etree.tostring(div_data[0], encoding='utf-8').decode()
        item['purchaser'] = ''
        item['create_time'] = str(datetime.datetime.now().strftime('%Y-%m-%d'))
        item['proxy'] = ''
        item['update_time'] = ''
        item['deleted'] = ''
        item['province'] = '青海省'
        item['base'] = ''
        item['items'] = ''
        item['data_source'] = '00694'
        item['end_time'] = ''
        item['status'] = ''
        item['serial'] = ''
        # print(item)
        yield item

