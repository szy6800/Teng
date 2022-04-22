# -*- coding: utf-8 -*-

# @Author : 石张毅
# @Site :https://www.landchina.com/resultNotice
# @introduce:青海省土地市场网
from copy import deepcopy

import scrapy
import json
import jsonpath

import re
class QhLandSpider(scrapy.Spider):
    name = 'qh_land'
    # allowed_domains = ['landchina.com']
    # start_urls = ['http://landchina.com/']

    # custom_settings = {
    #     'DEFAULT_REQUEST_HEADERS': {
    #         "Content-Type": "application/json",
    # }
    # }

    def start_requests(self):
        #构建post请求参数
        data = {"pageNum":6,"pageSize":10,"xzqDm":"6327","startDate":"","endDate":""}
        #发送post请求
        yield scrapy.FormRequest(
            url='https://api.landchina.com/tGdxm/result/list',
            method='POST',
            body=json.dumps(data),
            headers={'Content-Type': 'application/json'},
            callback=self.parse, dont_filter=True)

    def parse(self, response, **kwargs):
        # print(response.text)
        if response.status != 200:
            return
        js_text = json.loads(response.text)
        # 详情页id
        gdGuid = jsonpath.jsonpath(js_text,'$..gdGuid')
        # 行政区
        district = jsonpath.jsonpath(js_text,'$..xzqFullName')
        # 土地坐落
        address = jsonpath.jsonpath(js_text,'$..tdZl')
        # 总面积
        area = jsonpath.jsonpath(js_text,'$..gyMj')
        # 土地用途
        land_use = jsonpath.jsonpath(js_text,'$..tdYt')
        # 供应方式
        supply_mode = jsonpath.jsonpath(js_text,'$..gyFs')
        # 签订日期
        sign_date = jsonpath.jsonpath(js_text,'$..qdRq')

        for gdGuid, district,address,area,land_use,supply_mode,sign_date in zip(
                gdGuid,district,address,area,land_use,supply_mode,sign_date):
            item = dict()
            item['gdGuid'] = gdGuid
            item['district'] = district
            item['address'] = address
            item['area'] = int(area)*1000
            item['land_use'] = land_use
            sign_date = re.findall('\\d{4}-\\d{2}-\\d{2}',sign_date)[0]
            item['sign_date'] = sign_date
            item['supply_mode'] = supply_mode
            item['url'] = 'https://www.landchina.com/landSupplyDetail?id={}&type=%E4%BE%9B%E5%9C%B0%E7%BB%93%E6%9E%9C&path=0'.format(item['gdGuid'])
            data = {"gdGuid":"".format(item['gdGuid'])}
            # 发送post请求 请求详情页
            yield scrapy.FormRequest(
                url='https://api.landchina.com/tGdxm/result/detail',
                method='POST',
                headers={'Content-Type': 'application/json'},
                body=json.dumps(data),
                callback=self.parse_info, dont_filter=True,
                meta={'item': deepcopy(item)}
            )

    def parse_info(self, response):
        if response.status != 200:
            return
        item = response.meta['item']
        js_text = json.loads(response.text)
        # 省
        item['province'] = jsonpath.jsonpath(js_text, '$..province')[0]
        # 城市
        item['city'] = jsonpath.jsonpath(js_text, '$..city')[0]
        # 县
        try:
            item['county'] = jsonpath.jsonpath(js_text, '$..area')[0]
        except:
            item['county'] = item['city']
        # 电子监管号：
        item['ele_num'] = jsonpath.jsonpath(js_text, '$..dzBaBh')[0]
        # 项目名称
        item['pro_name'] = jsonpath.jsonpath(js_text, '$..xmMc')[0]
        # 土地来源
        item['land_source'] = jsonpath.jsonpath(js_text, '$..tdLy')[0]
        # 使用年限
        item['ser_life'] = jsonpath.jsonpath(js_text, '$..crNx')[0]
        # 行业
        item['industry'] = jsonpath.jsonpath(js_text, '$..hyFl')[0]
        # 土地等级
        item['land_level'] = jsonpath.jsonpath(js_text, '$..tdJb')[0]
        # 成交价格
        item['tran_price'] = jsonpath.jsonpath(js_text, '$..je')[0]
        # 土地权使用人
        item['srr'] = jsonpath.jsonpath(js_text, '$..srr')[0]
        # 批准单位
        item['pzJg'] = jsonpath.jsonpath(js_text, '$..pzJg')[0]
        # 批准号
        item['pzWh'] = jsonpath.jsonpath(js_text, '$..pzWh')[0]
        print(item)
        # print(response.text)


