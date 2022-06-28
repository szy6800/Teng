# -*- coding: utf-8 -*-

# @Author : 石张毅
# @Site : 工业和信息化部 https://www.miit.gov.cn/zwgk/tzcg/zfcg/index.html
# @introduce: 政府采购

import scrapy
import copy
from Qinghai.tools.utils import Utils_
from Qinghai.tools.DB_mysql import *
from Qinghai.tools.re_time import Times
import datetime
from lxml import etree
import jsonpath
import json


class MiitSpider(scrapy.Spider):
    name = 'miit'
    allowed_domains = ['miit.gov.cn']
    start_urls = ['http://miit.gov.cn/']

    def __init__(self, *args, **kwargs ):
        super(MiitSpider, self).__init__()
        self.cates = [
            {"cate": "zbgg", "pages": 1},  # 招标公告

        ]
        self.t = Times()
        self.c_time = datetime.datetime.utcnow() - datetime.timedelta(days=2)

    def start_requests(self):
        for each in self.cates:
            cate = each["cate"]
            pages = each["pages"]
            for p in range(pages):
                p = f"_{p+1}" if p else ""
                url = f"https://www.miit.gov.cn/api-gateway/jpaas-publish-server/front/page/build/unit?parseType=buildstatic&webId=8d828e408d90447786ddbe128d495e9e&tplSetId=209741b2109044b5b7695700b2bec37e&pageType=column&tagId=%E5%8F%B3%E4%BE%A7%E5%86%85%E5%AE%B9&editType=null&pageId=b78525590d014ea7b6d13548e9b7b2c0"
                yield scrapy.Request(url=url, callback=self.parse,dont_filter=True)

    def parse(self, response):
        json_text = json.loads(response.text)
        content = jsonpath.jsonpath(json_text, '$..html')[0]
        # print(content)
        html = etree.HTML(content)
        # print(response.text)
        item = {}
        # 列表页链接和发布时间
        list_url = html.xpath('//*[@class="page-content"]/ul/li//a/@href')
        # print(list_url)
        titles = html.xpath('//*[@class="page-content"]/ul/li//a/@title')
        # print(titles)
        pub_times = html.xpath('//*[@class="page-content"]/ul/li/a//following::span[1]/text()')
        # #循环遍历
        for href, title, pub_time in zip(list_url, titles, pub_times):
            # print(response.urljoin(href))
            item['link'] = response.urljoin(href.strip())
            item['title'] = title.strip()
            if item['title'] is None:
                continue
            PUBLISH = self.t.datetimes(pub_time)
            item['publish_time'] = PUBLISH.strftime('%Y-%m-%d')  # 发布时间
            # print(item['publish_time'])
            ctime = self.t.datetimes(item['publish_time'])
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
        item['uid'] = 'zf' + Utils_.md5_encrypt(item['title'] + item['link'] + item['publish_time'] )
        # 前言
        item['intro'] = ''
        item['abs'] = '1'
        from lxml import etree
        html = etree.HTML(response.text)
        div_data = html.xpath('//*[@id="con_con"]')
        item['content'] = etree.tostring(div_data[0], encoding='utf-8').decode()
        # 购买人
        item['purchaser'] = ''
        item['create_time'] = str(datetime.datetime.now().strftime('%Y-%m-%d'))
        # 代理人
        item['proxy'] = ''
        item['update_time'] = ''
        from Qinghai.tools.uredis import Redis_DB
        if Redis_DB().Redis_pd(item['uid']) is True:  #数据去重
            print(item['uid'], '\033[0;35m <=======此数据已采集=======> \033[0m')
            return
        item['deleted'] = ''
        # 省 份
        item['province'] = ''
        # 基础
        item['base'] = ''
        item['type'] = '政府采购'
        # 行业
        item['items'] = ''
        # 类型编号
        item['data_source'] = '00150'
        item['end_time'] = ''
        item['status'] = ''
        # 采购编号
        item['serial'] = ''

        yield item

