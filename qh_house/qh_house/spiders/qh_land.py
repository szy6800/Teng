# -*- coding: utf-8 -*-

# @Author : 石张毅
# @Site :https://www.landchina.com/resultNotice
# @introduce:青海省土地市场网

import scrapy
import json


class QhLandSpider(scrapy.Spider):
    name = 'qh_land'
    # allowed_domains = ['landchina.com']
    # start_urls = ['http://landchina.com/']
    custom_settings = {
        'DEFAULT_REQUEST_HEADERS': {
            "Content-Type": "application/json",

        }
    }

    def start_requests(self):
        #构建post请求参数
        data = {"pageNum": "600", "pageSize": "10", "xzqDm": "63", "startDate": "", "endDate": ""}
    #发送post请求
        yield scrapy.FormRequest(
            url='https://api.landchina.com/tGdxm/result/list',
            method='POST',
            body=json.dumps(data),
            callback=self.parse,dont_filter=True)

    def parse(self, response, **kwargs):
        print(response.text)
