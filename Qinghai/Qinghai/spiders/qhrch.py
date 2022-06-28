# -*- coding: utf-8 -*-

# @Author : 石张毅
# @Site :https://www.qhrch.com/index.php/zybecgg.html?pagesize=20&p=1 青海红十会医院
# @introduce: 招标公告

import scrapy
import copy
from Qinghai.tools.utils import Utils_
from Qinghai.tools.DB_mysql import *
from Qinghai.tools.re_time import Times
import datetime


class QhrchSpider(scrapy.Spider):
    name = 'qhrch'
    allowed_domains = ['qhrch.com']
    start_urls = ['http://qhrch.com/']

    def __init__(self, *args, **kwargs ):

        super(QhrchSpider, self).__init__()
        self.cates = [
            {"cate": "zbgg", "pages": 3},  # 招标公告
            {"cate": "zbgs", "pages": 3},  # 中标公示
            {"cate": "zybecgg", "pages": 3},  # 招议标再次公告
            {"cate": "ggbg", "pages": 3},  # 公告变更

        ]
        self.t = Times()
        self.c_time = datetime.datetime.utcnow() - datetime.timedelta(days=3)

    def start_requests(self):
        for each in self.cates:
            cate = each["cate"]
            pages = each["pages"]
            for p in range(1, pages):
                # p = f"_{p+1}" if p else ""
                url = f"https://www.qhrch.com/index.php/{cate}.html?pagesize=20&p={p}"
                yield scrapy.Request(url=url, callback=self.parse, dont_filter=True)

    def parse(self, response):
        # print(response.text)
        item = {}
        # 列表页链接和发布时间和标题
        list_url = response.xpath('//*[@class="textlist"]/li/a/@href').getall()
        # print(list_url)
        titles = response.xpath('//*[@class="textlist"]/li/a/text()').getall()
        # print(titles)
        pub_times = response.xpath('//*[@class="textlist"]/li/a/preceding::span[1]/text()').getall()
        if 'zbgg' in response.url:
            item['type'] = '招标公告'
        elif 'zbgs' in response.url:
            item['type'] = '中标公示'
        elif 'zybecgg' in response.url:
            item['type'] = '招议标再次公告'
        elif 'ggbg' in response.url:
            item['type'] = '公告变更'
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
            print(item['link'], item['publish_time'], item['title'], item['type'])
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
        from lxml import etree
        html = etree.HTML(response.text)
        div_data = html.xpath('//*[@class="InfoContent"]')
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
        item['province'] = '青海省'
        # 基础
        item['base'] = ''
        # 行业
        item['items'] = ''
        # 类型编号
        item['data_source'] = '00155'
        item['end_time'] = ''
        item['status'] = ''
        # 采购编号
        item['serial'] = ''

        yield item
