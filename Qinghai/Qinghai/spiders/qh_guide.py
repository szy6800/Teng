# -*- coding: utf-8 -*-

# @Time : 2022-07-27 15:26:24
# @Author : 石张毅
# @Site : http://www.guide.gov.cn/xxgk/List_wj.aspx?portalid=10&lmid=2787&pages=1
# @introduce: 贵德县人民政府

import scrapy
import copy
from Qinghai.tools.utils import Utils_
from Qinghai.tools.DB_mysql import *
from Qinghai.tools.re_time import Times
import datetime
from Qinghai.tools.uredis import Redis_DB

class GuideSpider(scrapy.Spider):
    name = 'qh_guide'

    def __init__(self, *args, **kwargs):
        super(GuideSpider, self).__init__()
        self.cates = [

        ]
        self.t = Times()
        self.c_time = datetime.datetime.utcnow() - datetime.timedelta(days=3)

    def start_requests(self):
        for i in range(1,3):
            url = 'http://www.guide.gov.cn/xxgk/List_wj.aspx?portalid=10&lmid=2787&pages={}'.format(i)
            yield scrapy.Request(url=url, callback=self.parse, dont_filter=True)

    def parse(self, response, **kwargs):
        # 列表页链接和发布时间
        count_list = response.xpath('//*[@class="lxzdls"]//tr[position()>1]')
        if count_list is []:
            return
        for count in count_list:
            item = dict()
            # 列表页链接和发布时间
            item['link'] = response.urljoin(count.xpath('.//a/@href').get())
            item['title'] = count.xpath('.//a/@title').get()
            if item['title'] is None:
                continue
            pub_time = count.xpath('./td[last()]/text()').get()
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
        div_data = html.xpath('//*[@id="Zoom2"]')
        item['content'] = etree.tostring(div_data[0], encoding='utf-8').decode()
        item['purchaser'] = ''
        item['create_time'] = str(datetime.datetime.now().strftime('%Y-%m-%d'))
        item['proxy'] = ''
        item['update_time'] = ''

        item['deleted'] = ''
        item['province'] = '青海省'
        item['base'] = ''
        item['type'] = '政府公告'
        item['items'] = ''
        item['data_source'] = '00691'
        item['end_time'] = ''
        item['status'] = ''
        item['serial'] = ''
        # print(item)
        yield item
