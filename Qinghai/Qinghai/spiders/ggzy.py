# -*- coding: utf-8 -*-

# @Author : 石张毅
# @Site :http://ggzy.jlbc.gov.cn 白城市公共资源交易平台


import scrapy
import scrapy
import copy
from Qinghai.tools.utils import Utils_
from Qinghai.tools.DB_mysql import *
from Qinghai.tools.re_time import Times
import datetime
from Qinghai.tools.uredis import Redis_DB

class GgzySpider(scrapy.Spider):
    name = 'ggzy'
    # allowed_domains = ['ggzy.jlbc.gov.cn']
    # start_urls = ['http://ggzy.jlbc.gov.cn/']
    def __init__(self, *args, **kwargs ):
        super(GgzySpider, self).__init__()
        self.cates = [
            {"cate": "003001", "pages": 3},  # 工程建设
            {"cate": "003002", "pages": 2},  # 政府采购
            {"cate": "003003", "pages": 2},  # 产权交易
            {"cate": "003004", "pages": 2},  # 国土及矿业产权交易


        ]
        self.t = Times()
        self.c_time = datetime.datetime.utcnow() - datetime.timedelta(days=2)

    def start_requests(self):
        for each in self.cates:
            cate = each["cate"]
            pages = each["pages"]
            for p in range(1, pages):
                if p == 1:
                    p = 'secondPage'
                url = f"http://ggzy.jlbc.gov.cn/jyxx/{cate}/{p}.html"
                yield scrapy.Request(url=url, callback=self.parse,dont_filter=True)

    def parse(self, response):
        # print(response.text)
        item = {}
        # 列表页链接和发布时间
        list_url = response.xpath('//*[@class="wb-data-infor"]/a/@href').getall()
        titles = response.xpath('//*[@class="wb-data-infor"]/a/text()[last()]').getall()
        pub_times = response.xpath('//*[@class="wb-data-infor"]/a/following::span[1]/text()').getall()
        # print(titles,pub_times)
        # 循环遍历
        for href, title, pub_time in zip(list_url, titles, pub_times):
            item['link'] = response.urljoin(href.strip())
            item['title'] = title.strip()
            PUBLISH = self.t.datetimes(pub_time.strip())
            item['publish_time'] = PUBLISH.strftime('%Y-%m-%d')  # 发布时间
            item['uid'] = 'zf' + Utils_.md5_encrypt(item['title'] + item['link'] + item['publish_time'])
            ctime = self.t.datetimes(item['publish_time'])
            if ctime < self.c_time:
                print('文章发布时间大于规定时间，不予采集', item['link'])
                return
            if Redis_DB().Redis_pd(item['uid']) is True:  # 数据去重
                print(item['uid'], '\033[0;35m <=======此数据已采集=======> \033[0m')
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
        div_data = html.xpath('//*[@id="commonarticle"]|//*[@class="news-article"]')
        item['content'] = etree.tostring(div_data[0], encoding='utf-8').decode()
        item['purchaser'] = ''
        item['create_time'] = str(datetime.datetime.now().strftime('%Y-%m-%d'))
        item['proxy'] = ''
        item['update_time'] = ''

        item['deleted'] = ''
        item['province'] = '吉林|白城'
        item['base'] = ''
        item['type'] = '招标公告'
        item['items'] = ''
        item['data_source'] = '00125'
        item['end_time'] = ''
        item['status'] = ''
        item['serial'] = ''

        yield item


