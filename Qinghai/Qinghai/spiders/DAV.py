# -*- coding: utf-8 -*-

# @Author : 石张毅
# @Site :DAV http://www.dav01.com/project/index.html


import scrapy
import copy
from Qinghai.tools.utils import Utils_
from Qinghai.tools.DB_mysql import *
from Qinghai.tools.re_time import Times
import datetime
from Qinghai.tools.uredis import Redis_DB

class DavSpider(scrapy.Spider):
    name = 'DAV'
    # allowed_domains = ['dav01.com']
    # start_urls = ['http://dav01.com/']

    def __init__(self, *args, **kwargs ):
        super(DavSpider, self).__init__()
        self.cates = [
            {"cate": "tender", "pages": 3},  # 招标公告
            {"cate": "xiangmu", "pages": 3},  # 基建项目

        ]
        self.t = Times()
        self.c_time = datetime.datetime.utcnow() - datetime.timedelta(days=4)

    def start_requests(self):
        for each in self.cates:
            cate = each["cate"]
            pages = each["pages"]
            for p in range(pages):
                p = f"-{p+1}" if p else ""
                url = f"http://www.dav01.com/project/{cate}/list-0-0-0-0{p}.html"
                yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        # print(response.text)
        item = {}
        # 列表页链接和发布时间
        list_url = response.xpath('//*[@class="ua-01"]/a/@href|//*[@class="ua-1"]/a/@href').getall()
        titles = response.xpath('//*[@class="ua-01"]/a/text()|//*[@class="ua-1"]/a/text()').getall()
        pub_times = response.xpath('//*[@class="ua-03"]/text()|//*[@class="ua-3"]/text()').getall()
        # 循环遍历
        for href, title, pub_time in zip(list_url, titles, pub_times):
            item['link'] = response.urljoin(href.strip())
            item['title'] = title.strip()
            if item['title'] is None:
                continue
            PUBLISH = self.t.datetimes(pub_time)
            item['publish_time'] = PUBLISH.strftime('%Y-%m-%d')  # 发布时间
            item['uid'] = 'zf' + Utils_.md5_encrypt(item['title'] + item['link'] + item['publish_time'])

            if Redis_DB().Redis_pd(item['uid']) is True:  # 数据去重
                print(item['uid'], '\033[0;35m <=======此数据已采集=======> \033[0m')
                return
            ctime = self.t.datetimes(item['publish_time'])
            #
            if ctime < self.c_time:
                print('文章发布时间大于规定时间，不予采集', item['link'])
                return
            # print(item['link'], item['publish_time'],item['title'])
            yield scrapy.Request(item['link'], callback=self.parse_info, meta={'item': copy.deepcopy(item)},dont_filter=True)

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
        div_data = html.xpath('//*[@class="newtext"]')
        item['content'] = etree.tostring(div_data[0], encoding='utf-8').decode()
        item['purchaser'] = ''
        item['create_time'] = str(datetime.datetime.now().strftime('%Y-%m-%d'))
        item['proxy'] = ''
        item['update_time'] = ''

        item['deleted'] = ''
        item['province'] = ''
        item['base'] = ''
        if 'tender' in item['link']:
            item['type'] = '招标公告'
        if 'project' in item['link']:
            item['type'] = '基建项目'
        item['items'] = ''
        item['data_source'] = '00120'
        item['end_time'] = ''
        item['status'] = ''
        item['serial'] = ''

        yield item
