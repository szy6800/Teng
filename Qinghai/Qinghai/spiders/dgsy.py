# -*- coding: utf-8 -*-

# @Author : 石张毅
# @Site :东莞实业投资控股集团 http://www.dgsy.com.cn
# @introduce:


import scrapy
import copy
from Qinghai.tools.utils import Utils_
from Qinghai.tools.DB_mysql import *
from Qinghai.tools.re_time import Times
import datetime

class DgsySpider(scrapy.Spider):
    name = 'dgsy'
    allowed_domains = ['dgsy.com.cn']
    start_urls = ['http://dgsy.com.cn/']

    def __init__(self, *args, **kwargs ):
        super(DgsySpider, self).__init__()
        self.cates = [
            {"cate": "zbgg", "pages": 1},  # 招标公告


        ]
        self.t = Times()
        self.c_time = datetime.datetime.utcnow() - datetime.timedelta(days=5)

    def start_requests(self):
        url = "http://www.dgsy.com.cn//www/main.jsp?f_treeCode=00190001"


        yield scrapy.FormRequest(url=url, callback=self.parse)

    def parse(self, response):
        # print(response.text)
        item = {}
    #     # 列表页链接和发布时间
        list_url = response.xpath('//*[@class="article_list"]//dd/a/@href').getall()
        # print(list_url)
        titles = response.xpath('//*[@class="article_list"]//dd/a/strong[1]/text()').getall()
        # print(titles)
        pub_times = response.xpath('//*[@class="article_list"]//dd/a/strong[1]/preceding::span[1]/text()').getall()
        #循环遍历
        for href, title, pub_time in zip(list_url, titles, pub_times):
            # print(response.urljoin(href))
            item['link'] = response.urljoin(href.strip())
            item['title'] = title.strip()
            if item['title'] is None:
                continue
            # pub_time = re.findall('\\d{4}-\\d{2}-\\d{2}', pub_time)[0]
            PUBLISH = self.t.datetimes(pub_time)
            item['publish_time'] = PUBLISH.strftime('%Y-%m-%d')  # 发布时间
            # print(item['link'], item['publish_time'],item['title'])
            ctime = self.t.datetimes(item['publish_time'])
            if ctime < self.c_time:
                print('文章发布时间大于规定时间，不予采集', item['link'])
                return
            yield scrapy.Request(item['link'], callback=self.parse_info, meta={'item': copy.deepcopy(item)},dont_filter=True)

    def parse_info(self, response):
        if response.status != 200:
            return
        item = response.meta['item']
        # 标题
        item['uuid'] = ''
        item['uid'] = 'zf' + Utils_.md5_encrypt(item['title'] + item['link'] + item['publish_time'] )
        item['intro'] = ''
        item['abs'] = '1'
        item['content'] = response.text
        # 购买人
        item['purchaser'] = ''
        item['create_time'] = str(datetime.datetime.now().strftime('%Y-%m-%d'))
        # 代理人
        item['proxy'] = ''
        item['update_time'] = ''
        item['deleted'] = ''
        # 省 份
        item['province'] = ''
        # 基础
        item['base'] = ''

        item['type'] = '招标公告'

        # 行业
        item['items'] = ''
        # 类型编号
        item['data_source'] = '00148'
        item['end_time'] = ''
        item['status'] = ''
        # 采购编号
        item['serial'] = ''

        yield item
