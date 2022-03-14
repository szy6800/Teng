# -*- coding: utf-8 -*-

# @Author : 石张毅
# @Site :https://cg.bnu.edu.cn/sfw_cms/e?page=cms.index 北京师范大学采购信息网
# @introduce: 北京师范大学 采购公告


import scrapy
import copy
from Qinghai.tools.utils import Utils_
from Qinghai.tools.DB_mysql import *
from Qinghai.tools.re_time import Times
import datetime
import jsonpath
import json


class BnuSpider(scrapy.Spider):
    name = 'bnu'
    # allowed_domains = ['bnu.edu.cn']
    # start_urls = ['http://bnu.edu.cn/']

    def __init__(self, *args, **kwargs ):
        super(BnuSpider, self).__init__()
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
        url = "https://cg.bnu.edu.cn/sfw_cms/e"

        formdata = {
            "t_": "0.75422885203361",
            "window_": "json",
            "start": "1",
            "limit": "25",
            "filter": "",
            "sort": "edate desc",
            "typeDetail": "XQ",
            "shoppingType": "",
            "type": "",
            "isEnd": "",
            "keywords": "",
            "request_method_": "ajax",
            "browser_": "notmsie",
            "page": "cms.psms.publish.query",
        }
        yield scrapy.FormRequest(url=url, formdata=formdata, callback=self.parse)

    def parse(self, response, **kwargs):
        item = {}
        json_text = json.loads(response.text)
        link_id = jsonpath.jsonpath(json_text, '$..syncId')
        titles = jsonpath.jsonpath(json_text, '$..subject')
        pub_times = jsonpath.jsonpath(json_text, '$..pdate')
        # 结束时间
        end_times = jsonpath.jsonpath(json_text, '$..edate')
        # print(titles,pub_times)
        # 循环遍历
        for href, title, pub_time, end_time in zip(link_id, titles, pub_times, end_times):
            # print(response.urljoin(href))
            item['link'] = 'https://cg.bnu.edu.cn/provider/#/publish/'+href
            item['title'] = title.strip()
            if item['title'] is None:
                continue
            end_time = self.t.datetimes(end_time)
            item['end_time'] = end_time.strftime('%Y-%m-%d')
            PUBLISH = self.t.datetimes(pub_time)
            item['publish_time'] = PUBLISH.strftime('%Y-%m-%d')  # 发布时间
            # print(item['publish_time'])
            ctime = self.t.datetimes(item['publish_time'])
            if ctime < self.c_time:
                print('文章发布时间大于规定时间，不予采集', item['link'])
                return
            # print(item['link'], item['publish_time'],item['title'],item['end_time'])
            yield scrapy.Request(item['link'], callback=self.parse_info, meta={'item': copy.deepcopy(item)},
                                 dont_filter=True)

    @staticmethod
    def parse_info(response):
        if response.status != 200:
            return
        item = response.meta['item']
        # 标题
        item['uuid'] = ''
        item['uid'] = 'zf' + Utils_.md5_encrypt(item['title'] + item['link'])
        item['intro'] = ''
        item['abs'] = ''
        item['content'] = response.text
        item['purchaser'] = ''
        item['create_time'] = str(datetime.datetime.now().strftime('%Y-%m-%d'))
        item['proxy'] = ''
        item['update_time'] = ''
        item['deleted'] = ''
        item['province'] = '北京市'
        item['base'] = ''
        item['base'] = ''
        item['type'] = '采购公告'
        item['items'] = ''
        item['data_source'] = '00131'
        item['status'] = ''
        item['serial'] = ''

        yield item

