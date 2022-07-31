# -*- coding: utf-8 -*-

# @Time : 2022-07-27 14:24:52
# @Author : 石张毅
# @Site :
# @introduce:

import scrapy
import jsonpath
import scrapy
import copy
from Qinghai.tools.utils import Utils_
from Qinghai.tools.DB_mysql import *
from Qinghai.tools.re_time import Times
import datetime
from Qinghai.tools.uredis import Redis_DB


class WestaportSpider(scrapy.Spider):
    name = 'qh_westaport'

    def __init__(self, *args, **kwargs):
        super(WestaportSpider, self).__init__()
        self.cates = [
            {"cate": "extId=5145322187743118692&lmTitle=%E9%87%87%E8%B4%AD%E5%85%AC%E5%91%8A&city=%E9%9D%92%E6%B5%B7", "pages": 2},  #
            {"cate": "extId=5145322187743118692&lmTitle=%E9%87%87%E8%B4%AD%E5%85%AC%E5%91%8A&city=$city", "pages": 2},  #

        ]
        self.t = Times()
        self.c_time = datetime.datetime.utcnow() - datetime.timedelta(days=2)

    def start_requests(self):
        for each in self.cates:
            cate = each["cate"]
            pages = each["pages"]
            for p in range(1, pages):
                # p = f"list-{p + 1}.html" if p else ""
                url = f"http://dzcg.westaport.com:8080/xbjc_las_web/register/supplierRegisterController/c/getThisChannelExtCity?{cate}&pages={p}"
                # print(url)
                yield scrapy.Request(url=url, callback=self.parse, dont_filter=True)

    def parse(self, response, **kwargs):
        # print(response.text)

        # 列表页链接和发布时间
        count_list = response.xpath('//*[@class="newsList1"]/ul/li')
        if count_list is []:
            return
        for count in count_list:
            item = dict()
            # 列表页链接和发布时间
            item['link'] = response.urljoin(count.xpath('./a/@type').get())
            item['title'] = count.xpath('./a/@title').get()

            if item['title'] is None:
                continue
            pub_time = count.xpath('./em/text()').get()
            PUBLISH = self.t.datetimes(pub_time)
            item['publish_time'] = PUBLISH.strftime('%Y-%m-%d')  # 发布时间
            # print(item['publish_time'],item['link'],item['title'])
            item['uid'] = 'zf' + Utils_.md5_encrypt(item['title'] + item['link'] + item['publish_time'])
            ctime = self.t.datetimes(item['publish_time'])
            if ctime < self.c_time:
                print('文章发布时间大于规定时间，不予采集', item['link'])
                return
            if Redis_DB().Redis_pd(item['uid']) is True:  # 数据去重
                print(item['uid'], '\033[0;35m <=======此数据已采集=======> \033[0m')
                continue
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
        div_data = html.xpath('//*[@class="zwgk_content"]')
        item['content'] = etree.tostring(div_data[0], encoding='utf-8').decode()
        item['purchaser'] = ''
        item['create_time'] = str(datetime.datetime.now().strftime('%Y-%m-%d'))
        item['proxy'] = ''
        item['update_time'] = ''

        item['deleted'] = ''
        item['province'] = '青海省'
        item['base'] = ''
        item['type'] = '采购公告'
        item['items'] = ''
        item['data_source'] = '00690'
        item['end_time'] = ''
        item['status'] = ''
        item['serial'] = ''
        # print(item)
        yield item
