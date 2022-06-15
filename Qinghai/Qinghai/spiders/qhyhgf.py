# -*- coding: utf-8 -*-

# @Author : 石张毅
# @Site :青海盐湖工业股份有限公司 https://www.qhyhgf.com/NewsInfoCategory?categoryId=326242&PageInfoId=343877
# @introduce: 公示公告
import json

import jsonpath
import scrapy
import copy
from Qinghai.tools.utils import Utils_
from Qinghai.tools.DB_mysql import *
from Qinghai.tools.re_time import Times
import datetime


class QhyhgfSpider(scrapy.Spider):
    name = 'qhyhgf'
    allowed_domains = ['qhyhgf.com']
    start_urls = ['http://qhyhgf.com/']

    def __init__(self, *args, **kwargs ):
        super(QhyhgfSpider, self).__init__()
        # self.cates = [
        #
        #     {"cate": "000", "pages": 2},  # 招标公告
        #     # {"cate": "001", "pages": 1},  # 变更公告
        #     # {"cate": "002", "pages": 1},  # 候选人公示
        #     # {"cate": "003", "pages": 1},  # 中标\流标公告
        #
        # ]
        self.t = Times()
        self.c_time = datetime.datetime.utcnow() - datetime.timedelta(days=2)

    def start_requests(self):
        url = "https://www.qhyhgf.com/Designer/Common/GetData"

        formdata = {
            "dataType": "news",
            "key": "",
            "pageIndex": "0",
            "pageSize": "10",
            "selectCategory": "326240",
            "selectId": "",
            "dateFormater": "yyyy-MM-dd",
            "orderByField": "createtime",
            "orderByType": "desc",
            "templateId": "0",
            "postData": "",
            "es": "false",
            "setTop": "true",
            "__RequestVerificationToken": "o7R2MCgA7rD1ULU-yTaeakb1EJWF-tpbAbMNaE3dSXLiXd3s4fsgp3nlc0Hu-OUvOINGe001Qr8LzG6t_ecATl-crGVupSMJAfUBY2YBN4s1",

        }
        yield scrapy.FormRequest(url=url, formdata=formdata, callback=self.parse)

    def parse(self, response):
        print(response.text)
        item = {}
        json_text = json.loads(response.text)
        list_url = jsonpath.jsonpath(json_text, "$..LinkUrl")
        # print(list_url)
        titles = jsonpath.jsonpath(json_text, "$..Name")
        # print(titles)
        pub_times = jsonpath.jsonpath(json_text, "$..QTime")
        # 循环遍历
        for href, title, pub_time in zip(list_url, titles, pub_times):
            # print(response.urljoin(href))
            item['link'] = response.urljoin(href.strip())
            item['title'] = title.strip()
            if item['title'] is None:
                continue
            PUBLISH = self.t.datetimes(pub_time)
            item['publish_time'] = PUBLISH.strftime('%Y-%m-%d')  # 发布时间
            print(item['link'], item['publish_time'], item['title'])
            ctime = self.t.datetimes(item['publish_time'])
            if ctime < self.c_time:
                print('文章发布时间大于规定时间，不予采集', item['link'])
                return
            yield scrapy.Request(item['link'], callback=self.parse_info, meta={'item': copy.deepcopy(item)},
                                 dont_filter=True)

    def parse_info(self, response):
        if response.status != 200:
            return
        item = response.meta['item']
        # 标题
        item['uuid'] = ''
        item['uid'] = 'zf' + Utils_.md5_encrypt(item['title'] + item['link'] + item['publish_time'])
        item['intro'] = ''
        item['abs'] = '1'
        item['content'] = response.text
        # 购买人
        item['purchaser'] = ''
        item['create_time'] = str(datetime.datetime.now().strftime('%Y-%m-%d'))
        # 代理人
        item['proxy'] = ''
        item['update_time'] = ''
        item['deleted'] = ''
        # 省 份
        item['province'] = '青海省'
        # 基础
        item['base'] = ''

        item['type'] = '招标公告'

        # 行业
        item['items'] = ''
        # 类型编号
        item['data_source'] = '00162'
        item['end_time'] = ''
        item['status'] = ''
        # 采购编号
        item['serial'] = ''

        yield item


