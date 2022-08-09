# -*- coding: utf-8 -*-

# @Time : 2022-08-08 16:35:57
# @Author : 石张毅
# @Site : https://www.obei.com.cn/obei-web-ec-ego/ego/home/noticeList.html?noticeType=2
# @introduce: 中国宝武钢铁集团有限公司

import scrapy
import re
import copy
from Qinghai.tools.utils import Utils_
from Qinghai.tools.DB_mysql import *
from Qinghai.tools.re_time import Times
import datetime
from Qinghai.tools.uredis import Redis_DB
import scrapy
import json

class ObeiSpider(scrapy.Spider):
    name = 'obei'

    def __init__(self, *args, **kwargs):
        super(ObeiSpider, self).__init__()
        self.cates = [
            {"cate": "1698", "pages": 2},
        ]
        self.t = Times()
        self.c_time = datetime.datetime.utcnow() - datetime.timedelta(days=3)

    def start_requests(self):
        url = 'https://www.obei.com.cn/obei-gateway/egogateway/n/ouyeelbuyAdmin/getNotice'
        for i in range(1, 2):
            data = {"page": '{}'.format(i), "rows": 10, "pageFlag": "addSelect", "memo": "obei", "noticeType": "2", "rfqMethod": "",
             "publicBiddingFlag": "", "ouName": "", "sidx": "requestEndDate", "sord": "desc"}
            yield scrapy.FormRequest(
                url=url,
                method='POST',
                body=json.dumps(data),
                headers={'Content-Type': 'application/json'},
                callback=self.parse,dont_filter=True,)

    def parse(self, response, **kwargs):
        json_text = json.loads(response.text)
        count_list = json_text['list']
        if count_list is []:
            return
        for count in count_list[0:1]:
            item = dict()
            # 列表页链接和发布时间
            ids = count['id']
            item['link'] = f'https://www.obei.com.cn/obei-web-ec-ego/ego/rfq/deploy/egoBusinessOpportunity.html#/id={ids}/rfqMethod=RAQ/orgCode=U04846/statusFlag=1'
            print(item['link'])
            item['title'] = count['title']
            if item['title'] is None:
                continue
            item['type'] = ''
            # pub_time = re.findall('\d{4}/\d{2}/\d{2}', response.text)[0].replace('/', '-')
            pub_time = count['requestEndDate']
            PUBLISH = self.t.datetimes(pub_time)
            item['publish_time'] = PUBLISH.strftime('%Y-%m-%d')  # 发布时间
            # print(item['publish_time'],item['link'],item['title'],item['type'])
            item['uid'] = 'zf' + Utils_.md5_encrypt(item['title'] + item['link'] + item['publish_time'])
            ctime = self.t.datetimes(item['publish_time'])
            if ctime < self.c_time:
                print('文章发布时间大于规定时间，不予采集', item['link'])
                return
            if Redis_DB().Redis_pd(item['uid']) is True:  # 数据去重
                print(item['uid'], '\033[0;35m <=======此数据已采集=======> \033[0m')
                return
            detail_data = {"rfqMethod":"RAQ","id":"{}".format(ids),"page":1,"rows":9999}
            yield scrapy.FormRequest(
                url='https://www.obei.com.cn/obei-gateway/ego-rfq-raq/n/transaction/announcementSup',
                method='POST',
                body=json.dumps(detail_data),
                headers={'Content-Type': 'application/json'},
                callback=self.parse_info,dont_filter=True,
                meta={'item': copy.deepcopy(item)},)

    def parse_info(self, response):
        json_text = json.loads(response.text)
        if response.status != 200:
            return
        item = response.meta['item']
        # 标题
        item['uuid'] = ''

        item['intro'] = ''
        item['abs'] = '1'
        # from lxml import etree
        # html = etree.HTML(response.text)
        # div_data = html.xpath('//*[@class="InfoContent"]')
        content = json_text['data']['requestDto']['requestBusiTerms']
        item['content'] = json_text['data']['requestDto']['ouRfqNum']+content
        item['purchaser'] = ''
        item['create_time'] = str(datetime.datetime.now().strftime('%Y-%m-%d'))
        item['proxy'] = ''
        item['update_time'] = ''
        item['deleted'] = ''
        item['province'] = ''
        item['base'] = ''
        item['items'] = ''
        item['data_source'] = '00723'
        item['end_time'] = ''
        item['status'] = ''
        item['serial'] = ''
        # print(item)
        yield item





