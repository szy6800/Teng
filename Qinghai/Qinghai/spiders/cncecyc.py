# -*- coding: utf-8 -*-

# @Time : 2022-08-10 10:37:11
# @Author : 石张毅
# @Site : http://bid.cncecyc.com/cms/channel/ywgg1hw/index.htm
# http://bid.cncecyc.com/cms/channel/ywgg1gc/index.htm
# http://bid.cncecyc.com/cms/channel/ywgg1fw/index.htm
# http://bid.cncecyc.com/cms/channel/ywgg2hw/index.htm
# http://bid.cncecyc.com/cms/channel/ywgg2gc/index.htm
# http://bid.cncecyc.com/cms/channel/ywgg2fw/index.htm
# http://bid.cncecyc.com/cms/channel/ywgg4hw/index.htm
# http://bid.cncecyc.com/cms/channel/ywgg4gc/index.htm
# http://bid.cncecyc.com/cms/channel/ywgg4fw/index.htm
# @introduce: 中国化学电子招标投标交易平台

import scrapy
from Qinghai.tools.uredis import Redis_DB
from Qinghai.tools.utils import Utils_
from Qinghai.tools.DB_mysql import *
from Qinghai.tools.re_time import Times
import datetime
from Qinghai.tools.uredis import Redis_DB
import copy


class CncecycSpider(scrapy.Spider):
    name = 'cncecyc'
    def __init__(self, *args, **kwargs):
        super(CncecycSpider, self).__init__()
        self.cates = [
            {"cate": "ywgg1hw", "pages": 3},  # 招中标信息
            {"cate": "ywgg1gc", "pages": 3},  # 招中标信息
            {"cate": "ywgg1fw", "pages": 3},  # 招中标信息
            {"cate": "ywgg2hw", "pages": 3},  # 招中标信息
            {"cate": "ywgg2gc", "pages": 3},  # 招中标信息
            {"cate": "ywgg2fw", "pages": 3},  # 招中标信息
            {"cate": "ywgg4hw", "pages": 3},  # 招中标信息
            {"cate": "ywgg4gc", "pages": 3},  # 招中标信息
            {"cate": "ywgg4fw", "pages": 3},  # 招中标信息
        ]
        self.t = Times()
        self.c_time = datetime.datetime.utcnow() - datetime.timedelta(days=3)

    def start_requests(self):
        for each in self.cates:
            cate = each["cate"]
            pages = each["pages"]
            for p in range(1, pages):
                url = f"http://bid.cncecyc.com/cms/channel/{cate}/index.htm?pageNo={p}"
                yield scrapy.Request(url=url, callback=self.parse, dont_filter=True)


    def parse(self, response, **kwargs):
        # 列表页链接和发布时间
        count_list = response.xpath('//*[@id="list1"]/li')
        types = response.xpath('//*[@class="m-hd"]/h2/text()').get()
        if count_list is []:
            return
        for count in count_list:
            item = dict()
            # 列表页链接和发布时间
            item['link'] = response.urljoin(count.xpath('./a/@href').get())
            item['title'] = count.xpath('./a/@title').get()
            if item['title'] is None:
                continue
            item['type'] = types
            # pub_time = re.findall('\d{4}/\d{2}/\d{2}', response.text)[0].replace('/', '-')
            pub_time = count.xpath('.//span[@class="bidDate"]/text()').get()
            PUBLISH = self.t.datetimes(pub_time)
            item['publish_time'] = PUBLISH.strftime('%Y-%m-%d')  # 发布时间
            #print(item['publish_time'],item['link'],item['title'],item['type'])
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
        div_data = html.xpath('//*[@class="ninfo-con"]')
        item['content'] = etree.tostring(div_data[0], encoding='utf-8').decode()
        item['purchaser'] = ''
        item['create_time'] = str(datetime.datetime.now().strftime('%Y-%m-%d'))
        item['proxy'] = ''
        item['update_time'] = ''
        item['deleted'] = ''
        item['province'] = ''
        item['base'] = ''
        item['items'] = ''
        item['data_source'] = '00724'
        item['end_time'] = ''
        item['status'] = ''
        item['serial'] = ''
        # print(item)
        yield item
