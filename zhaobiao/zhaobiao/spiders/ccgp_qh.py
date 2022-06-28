# -*- coding: utf-8 -*-
import datetime
import json

import scrapy
import re
import time

from bs4 import BeautifulSoup
from copy import deepcopy
from zhaobiao.items import ZhaobiaoItem
from zhaobiao.tools.DB_mysql import *
from zhaobiao.tools.re_time import Times
from zhaobiao.tools.utils import Utils_


def bo(url):
    browser = Utils_.login('')
    browser.get(url)
    browser.switch_to.frame('iframe')
    page_source = browser.page_source
    soup = BeautifulSoup(page_source, "lxml")
    content = str(soup.select('.view')[0])
    browser.quit()

    return content

class CcgpQhSpider(scrapy.Spider):
    name = 'ccgp_qh'
    # allowed_domains = ['www.c']
    # start_urls = ['http://www.c/']

    def __init__(self, *args, **kwargs):
        super(CcgpQhSpider, self).__init__()
        self.L = {
            '1': '采购公示',
            '2': '公开招标',
            '3009': '邀请招标公告',
            '3002': '竞争性谈判公告',
            '3011': '竞争性协商公告',
            '3003': '询价采购公告',
            '4': '中标公告',
            '3': '变更公告',
            '8888': '资格预审公告',
        }
        self.t = Times()
        self.c_time = datetime.datetime.utcnow() - datetime.timedelta(days=2)

    def start_requests(self):
        for k,v in self.L.items():
            new_url = 'http://www.ccgp-qinghai.gov.cn/front/search/category'
            page = 1
            payload = {
                "categoryCode": f"ZcyAnnouncement{k}",
                # "categoryCode": 'ZcyAnnouncement4',
                "pageNo": 1,
                "pageSize": 15,
                "utm": "sites_group_front.5b1ba037.0.0.56b5e0a0929311ebb174c5a2368ee3da"
            }
            headers = {
                "Accept": "*/*",
                "Content-Type": "application/json",
                "Cookie": "_zcy_log_client_uuid=67414810-a58f-11eb-97d1-11668455ef94; acw_tc=76b20fe216239144357253684e076eb90b4032901511acd0efb4f8d4d6d4eb",
                "Referer": "http://www.ccgp-qinghai.gov.cn/ZcyAnnouncement/ZcyAnnouncement3/index.html?utm=sites_group_front.5b1ba037.0.0.56b5e0a0929311ebb174c5a2368ee3da",
            }
            yield scrapy.Request(new_url, headers=headers, body=json.dumps(payload), method="POST", callback=self.parse, meta={'page':page,'k':k})
            # yield scrapy.FormRequest(new_url, headers=headers, formdata=payload, callback=self.parse)

    def parse(self, response):
        page = response.meta['page']
        k = response.meta['k']
        count_list = json.loads(response.text)['hits']['hits']
        for count in count_list:
            item = ZhaobiaoItem()
            item['uuid'] = ''
            item['title'] = count['_source']['title']
            if item['title'] == None:
                continue
            item['link'] = 'http://www.ccgp-qinghai.gov.cn' + count['_source']['url']
            # item['id'] = ''
            item['uid'] = 'zf' + Utils_.md5_encrypt(item['title'] + item['link'] + item['publish_time'] )
            item['intro'] = ''
            item['abs'] = '1'
            # item['content'] = ''
            PUBLISH = self.t.datetimes(str(count['_source']['publishDate']))
            item['publish_time'] = PUBLISH.strftime('%Y-%m-%d')  # 发布时间
            ctime = self.t.datetimes(item['publish_time'])
            # print(item['publishdata'])
            # print(type(item['publishdata']))
            if ctime < self.c_time:
                print('文章发布时间大于一个月，不予采集', item['link'])
                return
            item['purchaser'] = ''
            item['proxy'] = ''
            # item['create_time'] = item['publish_time']
            item['create_time'] = str(datetime.datetime.now().strftime('%Y-%m-%d'))
            item['update_time'] = ''
        from Qinghai.tools.uredis import Redis_DB
        if Redis_DB().Redis_pd(item['uid']) is True:  #数据去重
            print(item['uid'], '\033[0;35m <=======此数据已采集=======> \033[0m')
            return
            item['deleted'] = ''
            try:
                item['province'] = count['_source']['districtName']
            except:
                item['province'] = ''
            item['base'] = ''
            try:
                item['type'] = count['_source']['pathName']
            except:
                item['type'] = ''
            try:
                item['items'] = count['_source']['gpCatalogType']
            except:
                item['items'] = ''
            item['data_source'] = '00002'
            item['end_time'] = ''
            item['status'] = ''
            item['serial'] = ''
            item['content'] = bo(item['link'])
            yield item
            time.sleep(0.5)
            # yield scrapy.Request(item['link'], callback=self.son_parse, meta={'item': deepcopy(item)})

        new_url = 'http://www.ccgp-qinghai.gov.cn/front/search/category'
        page += 1
        payload = {
            "categoryCode": f"ZcyAnnouncement{k}",
            # "categoryCode": 'ZcyAnnouncement4',
            "pageNo": page,
            "pageSize": 15,
            "utm": "sites_group_front.5b1ba037.0.0.56b5e0a0929311ebb174c5a2368ee3da"
        }
        headers = {
            "Accept": "*/*",
            "Content-Type": "application/json",
            "Cookie": "_zcy_log_client_uuid=67414810-a58f-11eb-97d1-11668455ef94; acw_tc=76b20fe216239144357253684e076eb90b4032901511acd0efb4f8d4d6d4eb",
            "Referer": "http://www.ccgp-qinghai.gov.cn/ZcyAnnouncement/ZcyAnnouncement3/index.html?utm=sites_group_front.5b1ba037.0.0.56b5e0a0929311ebb174c5a2368ee3da",
        }
        yield scrapy.Request(new_url, headers=headers, body=json.dumps(payload), method="POST", callback=self.parse, meta={'page':page,'k':k})

    def son_parse(self, response):
        time.sleep(1)
        if response.status != 200:
            return
        item = response.meta['item']
        # print(response.text)
        from lxml import etree
        html = etree.HTML(response.text)
        div_data = html.xpath('//*[@id="news_detail1"]')
        item['content'] = etree.tostring(div_data[0], encoding='utf-8').decode()
        # print(item)
        time.sleep(1)
        yield item