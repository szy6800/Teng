# -*- coding: utf-8 -*-

# @Author : 石张毅
# @Site : http://www.tobaccobid.com/web/listsestb2.html 烟草行业招投标信息平台
# @introduce: 招标公告  中标公告 招标变更

import scrapy
import copy
from Qinghai.tools.utils import Utils_
from Qinghai.tools.DB_mysql import *
from Qinghai.tools.re_time import Times
import datetime
from Qinghai.tools.uredis import Redis_DB

class TobaccobidSpider(scrapy.Spider):
    name = 'tobaccobid'
    allowed_domains = ['tobaccobid.com']
    start_urls = ['http://tobaccobid.com/']

    def __init__(self, *args, **kwargs ):

        super(TobaccobidSpider, self).__init__()
        self.cates = [
            {"cate": "listsestb", "pages": 5},  # 招标公告
            {"cate": "listseszb", "pages": 5},  # 中标公告
            {"cate": "listsesgb", "pages": 5},  # 招标变更

        ]
        self.t = Times()
        self.c_time = datetime.datetime.utcnow() - datetime.timedelta(days=3)

    def start_requests(self):
        for each in self.cates:
            cate = each["cate"]
            pages = each["pages"]
            for p in range(1, pages):
                # p = f"_{p+1}" if p else ""
                url = f"http://www.tobaccobid.com/web/{cate}{p}.html"
                yield scrapy.Request(url=url, callback=self.parse, dont_filter=True)

    def parse(self, response):
        # print(response.text)
        item = {}
        # 列表页链接和发布时间和标题
        list_url = response.xpath('//*[@class="lie"]/li/a/@href').getall()
        # print(list_url)
        titles = response.xpath('//*[@class="lie"]/li/a/@title').getall()
        # print(titles)
        pub_times = response.xpath('//span[@class="fr"]/text()').getall()
        if 'listsestb' in response.url:
            item['type'] = '招标公告'
        elif 'listseszb' in response.url:
            item['type'] = '中标公示'
        elif 'listsesgb' in response.url:
            item['type'] = '招标变更'
        # print(item['type'])
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
            item['uid'] = 'zf' + Utils_.md5_encrypt(item['title'] + item['link'] + item['publish_time'])

            if Redis_DB().Redis_pd(item['uid']) is True:  # 数据去重
                print(item['uid'], '\033[0;35m <=======此数据已采集=======> \033[0m')
                return
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

        item['intro'] = ''
        item['abs'] = '1'
        from lxml import etree
        html = etree.HTML(response.text)
        div_data = html.xpath('//*[@class="righ1 fr"]')
        item['content'] = etree.tostring(div_data[0], encoding='utf-8').decode()
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
        # 行业
        item['items'] = ''
        # 类型编号
        item['data_source'] = '00154'
        item['end_time'] = ''
        item['status'] = ''
        # 采购编号
        item['serial'] = ''

        yield item
