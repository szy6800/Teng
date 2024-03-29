# -*- coding: utf-8 -*-

# @Author : 石张毅
# @Site :http://ggzyjy.bjchy.gov.cn  朝阳区公共资源交易平台
# @introduce: 招标公告
import re
import scrapy
import copy
from Qinghai.tools.utils import Utils_
from Qinghai.tools.DB_mysql import *
from Qinghai.tools.re_time import Times
import datetime

from Qinghai.tools.uredis import Redis_DB
class BjchySpider(scrapy.Spider):
    name = 'bjchy'
    allowed_domains = ['bjchy.gov.cn']

    def __init__(self, *args, **kwargs ):
        super(BjchySpider, self).__init__()
        self.cates = [
            {"cate": "zbgg", "pages": 1},  # 招标公告

        ]
        self.t = Times()
        self.c_time = datetime.datetime.utcnow() - datetime.timedelta(days=5)

    def start_requests(self):
        url = f"http://ggzyjy.bjchy.gov.cn/cyggzy/search.jspx?q=%25E6%258B%259B%25E6%25A0%2587%25E5%2585%25AC%25E5%2591%258A###"
        yield scrapy.Request(url=url, callback=self.parse,dont_filter=True)

    def parse(self, response):
        # print(response.text)
        item = {}
        # 列表页链接和发布时间
        list_url = response.xpath('//*[@class="article-list3-t"]/a/@href').getall()
        # print(list_url)
        titles = response.xpath('//*[@class="article-list3-t"]/a/@title').getall()
        # print(titles)
        pub_times = response.xpath('//*[@class="article-list3-t"]/a/following::div[1]/text()').getall()
        #循环遍历
        for href, title, pub_time in zip(list_url, titles, pub_times):
            # print(response.urljoin(href))
            item['link'] = response.urljoin(href.strip())
            item['title'] = title.strip()
            if item['title'] is None:
                continue
            pub_time = re.findall('\\d{4}.\\d{2}.\\d{2}', pub_time)[0]
            PUBLISH = self.t.datetimes(pub_time)
            item['publish_time'] = PUBLISH.strftime('%Y-%m-%d')
            item['uid'] = 'zf' + Utils_.md5_encrypt(item['title'] + item['link'] + item['publish_time'])
            if Redis_DB().Redis_pd(item['uid']) is True:  # 数据去重
                print(item['uid'], '\033[0;35m <=======此数据已采集=======> \033[0m')
                return
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

        item['intro'] = ''
        item['abs'] = '1'
        from lxml import etree
        html = etree.HTML(response.text)
        div_data = html.xpath('//*[@id="content"]')
        item['content'] = etree.tostring(div_data[0], encoding='utf-8').decode()
        item['purchaser'] = ''
        item['create_time'] = str(datetime.datetime.now().strftime('%Y-%m-%d'))
        item['proxy'] = ''
        item['update_time'] = ''

        item['deleted'] = ''
        item['province'] = ''
        item['base'] = ''
        item['type'] = '招标公告'
        item['items'] = ''
        item['data_source'] = '00145'
        item['end_time'] = ''
        item['status'] = ''
        item['serial'] = ''

        yield item

