# -*- coding: utf-8 -*-
import datetime
import json
import scrapy
import copy
from gansuxinwen.items import GansuxinwenItem
from gansuxinwen.tools.DB_mysql import *
from gansuxinwen.tools.re_time import Times
from gansuxinwen.tools.utils import Utils_
from gansuxinwen.tools.DB_redis import Redis_DB

class FzggSpider(scrapy.Spider):
    name = 'fzgg'
    # allowed_domains = ['www.ccc']
    # start_urls = ['http://www.ccc/']

    def __init__(self, *args, **kwargs):
        super(FzggSpider, self).__init__()
        self.L = {
            'zbgg': '',
        }
        self.t = Times()
        self.c_time = datetime.datetime.utcnow() - datetime.timedelta(days=38)

    def start_requests(self):
        new_url = 'http://www.aii-alliance.org/index/c144.html?page=1'
        yield scrapy.Request(new_url, callback=self.parse)

    def parse(self, response, *args):
        # 列表页链接和发布时间
        list_url = response.xpath('//*[@class="lmdt-news-item-right"]/a/@href').getall()
        # print(list_url)
        titles = response.xpath('//*[@class="lmdt-news-item-right"]/a/@title').getall()
        pub_times = response.xpath('//*[@class="lmdt-news-item-right"]/div[1]/text()').getall()
        # print(titles,pub_times)
        # 循环遍历
        for href, title, pub_time in zip(list_url, titles, pub_times):
            item={}
            # print(response.urljoin(href))
            item['link'] = response.urljoin(href.strip())
            item['title'] = title.strip()
            if item['title'] is None:
                continue
            pub_time = pub_time.replace('.','-')
            PUBLISH = self.t.datetimes(pub_time)
            item['publish_time'] = PUBLISH.strftime('%Y-%m-%d')  # 发布
            item['uid'] = 'zf' + Utils_.md5_encrypt(item['title'] + item['link'] + item['publish_time'])
            if Redis_DB().Redis_pd(item['uid']) is True:  # 数据去重
                print(item['uid'], '\033[0;35m <=======此数据已采集=======> \033[0m')
                return
            # print(item['publish_time'])
            ctime = self.t.datetimes(item['publish_time'])
            if ctime < self.c_time:
                print('文章发布时间大于规定时间，不予采集', item['link'])
                return
            item['province'] = ''
            item['create_time'] = str(datetime.datetime.now().strftime('%Y-%m-%d'))
            item['author'] = '工业互联网产业联盟'
            item['data_source'] = '00666'
            item['status'] = ''
            item['base'] = ''

            # print(item['link'], item['publish_time'],item['title'])
            yield scrapy.Request(item['link'], callback=self.parse_info, meta={'item': copy.deepcopy(item)},
                                 dont_filter=True)


    @staticmethod
    def parse_info(response):
        if response.status != 200:
            return
        item = response.meta['item']
        # print(response.text)
        from lxml import etree
        html = etree.HTML(response.text)
        div_data = html.xpath('//*[@class="news-content"]')
        item['content'] = etree.tostring(div_data[0], encoding='utf-8').decode()
        yield item




