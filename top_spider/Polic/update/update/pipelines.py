# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import requests
import json


class UpdatePipeline(object):
    def process_item(self, item, spider):
        # url = 'http://47.94.230.63:18080/policies/sync'
        url = 'http://192.168.3.213:18090/doc/sync'
        # url = 'http://api.yqypt.com/policies/sync'
        # headers = {'content-type': 'application/json',
        # url = 'http://api.yqypt.com/policies/sync'
        headers = {'content-type': 'application/json',}
        datas = json.dumps(item)
        res = requests.post(url, data=datas, headers=headers)
        res.encoding = res.apparent_encoding
        print('****************************************************')
        print(datas)
        print(res.text)
