# -*- coding: utf-8 -*-

# @Author : 石张毅
# @Site :
# @introduce:http://ec.ccccltd.cn/PMS/gysmore.shtml?id=sjN7r9ttBwLI2dpg4DQpQb68XreXjaqknBMygP8dAEQ57TILyRtTnCZX1hIiXHcc1Ra16D6TzZdblRFD/JXcCd5FP7Ek60ksxl9KkyODirY=
import json
import re

import scrapy
import copy
from Qinghai.tools.utils import Utils_
from Qinghai.tools.DB_mysql import *
from Qinghai.tools.re_time import Times
import datetime
from Qinghai.tools.uredis import Redis_DB

class CcccltdSpider(scrapy.Spider):
    name = 'ccccltd'
    allowed_domains = ['ccccltd.cn']
    start_urls = ['http://ccccltd.cn/']

    def __init__(self, *args, **kwargs ):
        super(CcccltdSpider, self).__init__()
        # self.cates = [
        #
        # ]
        self.t = Times()
        self.c_time = datetime.datetime.utcnow() - datetime.timedelta(days=5)

    def start_requests(self):
        url = "http://ec.ccccltd.cn/PMS/gysmore.shtml?id=sjN7r9ttBwLI2dpg4DQpQb68XreXjaqknBMygP8dAEQ57TILyRtTnCZX1hIiXHcc1Ra16D6TzZdblRFD/JXcCd5FP7Ek60ksxl9KkyODirY="
        for d1, d2 in zip(range(0,5), range(1,6)):
            formdata = {
                "pid": "",
                "announcetstrtime_from": "",
                "announcetstrtime_to": "",
                "announcetitle": "",
                "dalei": "",
                "VENUS_PAGE_NO_KEY_INPUT": "{}".format(d1),
                "VENUS_PAGE_NO_KEY": "{}".format(d2),
                "VENUS_PAGE_COUNT_KEY": "6168",
                "VENUS_PAGE_SIZE_KEY": "15",
            }
            yield scrapy.FormRequest(url=url, formdata=formdata, callback=self.parse)

    def parse(self, response):
        item = {}
        # 列表页链接和发布时间
        list_url = response.xpath('//*[@class="listCss"]/a/@href').getall()
        # print(list_url)
        titles = response.xpath('//*[@class="listCss"]/a/text()').getall()
        # print(titles)
        pub_times = response.xpath('//*[@class="listCss"]/a/following::td[1]/text()').getall()
        # 循环遍历
        for href, title, pub_time in zip(list_url, titles, pub_times):
            # print(href)
            try:
                link = re.findall("javaScript:goAnnounceDetail\(\'([^\']+)\'\);" ,href)[0]
                links = 'http://ec.ccccltd.cn/PMS/moredetail.shtml?id=' + link
                links.replace('\n', '').replace('\r', '').replace('\r\n', '')
                item['link'] = links

                item['title'] = title.strip()
                if item['title'] is None:
                    continue
                PUBLISH = self.t.datetimes(pub_time.strip())
                item['publish_time'] = PUBLISH.strftime('%Y-%m-%d')  # 发布时间
                item['uid'] = 'zf' + Utils_.md5_encrypt(item['title'] + item['link'] + item['publish_time'])

                if Redis_DB().Redis_pd(item['uid']) is True:  # 数据去重
                    print(item['uid'], '\033[0;35m <=======此数据已采集=======> \033[0m')
                    return
                ctime = self.t.datetimes(item['publish_time'])
                if ctime < self.c_time:
                    print('文章发布时间大于规定时间，不予采集', item['link'])
                    return
                yield scrapy.Request(item['link'], callback=self.parse_info, meta={'item': copy.deepcopy(item)},
                                     dont_filter=True)

            except Exception as e:
                print(e)

    def parse_info(self,response):
        if response.status != 200:
            return
        item = response.meta['item']
        # 标题
        item['uuid'] = ''
        item['intro'] = ''
        item['abs'] = '1'
        from lxml import etree
        html = etree.HTML(response.text)
        div_data = html.xpath('//*[@class="tab_content"]')
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

        item['type'] = response.xpath('//*[@id="subnav"]/span/text()').get()
        # 行业
        item['items'] = ''
        # 类型编号
        item['data_source'] = '00172'

        item['end_time'] = ''

        item['status'] = ''
        # 采购编号
        item['serial'] = ''
        # print(item)
        yield item




