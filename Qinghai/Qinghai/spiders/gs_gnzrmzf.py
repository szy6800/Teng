# -*- coding: utf-8 -*-

# @Author : 石张毅
# @Site : http://ggzyjy.gnzrmzf.gov.cn/f/newtrade/annogoods/tradeIndex
# @introduce: 甘肃省紫色字幕 甘南州公共资源交易中心 招标公告

import scrapy
import scrapy
import copy
from Qinghai.tools.utils import Utils_
from Qinghai.tools.DB_mysql import *
from Qinghai.tools.re_time import Times
from lxml import etree
import datetime
import jsonpath
import json
import re

class GsGnzrmzfSpider(scrapy.Spider):
    name = 'gs_gnzrmzf'

    def __init__(self, *args, **kwargs):
        super(GsGnzrmzfSpider, self).__init__()
        # self.cates = [
        #
        #     {"cate": "000", "pages": 2},  # 招标公告
        #     # {"cate": "001", "pages": 1},  # 变更公告
        #     # {"cate": "002", "pages": 1},  # 候选人公示
        #     # {"cate": "003", "pages": 1},  # 中标\流标公告
        #
        # ]
        self.t = Times()
        self.c_time = datetime.datetime.utcnow() - datetime.timedelta(days=5)

    def start_requests(self):
        for i in range(0, 10):
            url = "http://ggzyjy.gnzrmzf.gov.cn/f/newtrade/annogoods/getAnnoList"
            formdata = {
                "pageNo": "{}".format(i),
                "pageSize": "20",
                "tradeStatus": "0",
                "prjpropertycode": "1,2,3,4,5,6,7,8,9,10,11",
                # "prjpropertycode": "21,22,23,24",
                # "prjpropertycode": "31",
                # "prjpropertycode": "13,14,15,16,18,19,20",
                # "prjpropertycode": "600",
                "tradeArea": "14",
                "projectname": "",
                # "tabType": "2",
                "tabType": "1",
                "tradeType": "",
            }
            yield scrapy.FormRequest(url=url, formdata=formdata, callback=self.parse)

    def parse(self, response, **kwargs):
        list_url = response.xpath('//*[@class="byTradingDetailTitle clear"]/a/@href').getall()
        pub_times = response.xpath('//*[@class="byTradingDetailTime"]/text()').getall()
        # print(titles)
        # 循环遍历
        for href, pub_time in zip(list_url, pub_times):
            item = dict()
            item['link'] = response.urljoin(href)
            pub_time = re.findall('\\d{4}-\\d{2}-\\d{2}', pub_time)[0]
            PUBLISH = self.t.datetimes(pub_time)
            item['publish_time'] = PUBLISH.strftime('%Y-%m-%d')  # 发布时间
            ctime = self.t.datetimes(item['publish_time'])
            if ctime < self.c_time:
                print('文章发布时间大于规定时间，不予采集', item['link'])
                return

            yield scrapy.Request(item['link'], callback=self.parse_info, meta={'item': copy.deepcopy(item)},
                                 dont_filter=True)


    def parse_info(self,response):
        if response.status != 200:
            return
        item = response.meta['item']
        item['title'] = response.xpath('//h2/text()').get()
        # 标题
        item['uuid'] = ''
        item['uid'] = 'zf' + Utils_.md5_encrypt(item['title'] + item['link'] + item['publish_time'])
        item['intro'] = ''
        item['abs'] = '1'
        html = etree.HTML(response.text)
        div_data = html.xpath('//*[@class="jxTradingMainLeft"]')[0]
        item['content'] =etree.tostring(div_data, encoding='utf-8').decode()

        item['purchaser'] = response.xpath("//*[contains(text(),'招标人：')]/following::td[1]/text()").get()
        item['create_time'] = str(datetime.datetime.now().strftime('%Y-%m-%d'))
        item['proxy'] = ''
        item['update_time'] = ''
        item['deleted'] = ''
        item['province'] = '甘肃省'
        item['base'] = ''
        item['type'] = '招标公告'
        item['items'] = response.xpath("//*[contains(text(),'项目类型：')]/following::td[1]/text()").get()
        item['data_source'] = '00397'
        item['end_time'] = ''
        item['status'] = ''
        item['serial'] = response.xpath("//*[contains(text(),'项目编号：')]/following::td[1]/text()").get()

        yield item



