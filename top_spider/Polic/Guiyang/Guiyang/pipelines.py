# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import json,requests
class GuiyangPipeline(object):

    def process_item(self, item, spider):
        url = 'http://api.yqypt.com/v2/policies/sync'
        # url = 'https://api.yqypt.com/v2/policies/sync'
        token = "bfa89e563d9509fbc5c6503dd50faf2e"
        headers = {'content-type': 'application/json',
                   'syncToken': token}
        datas = json.dumps(item)
        res = requests.post(url, data=datas, headers=headers)
        res.encoding = res.apparent_encoding
        print('****************************************************')
        print(datas)
        print(res.text)




class GuiyangtePipeline(object):

    def process_item(self, item, spider):
        url = 'https://www.qjos.cn/developers-server/rest/article/save'
        # url = 'https://api.yqypt.com/v2/policies/sync'
        headers = {
            "Content-Type": "application/json",
            "Cookie": "__dp_tk__=3f14aa0bfb33459f91959e502e7fb063",
            "Host": "www.qjos.cn",
            "Origin": "https://www.qjos.cn",
            "Referer": "https://www.qjos.cn/draft/editor/new?t=article",
        "Token": "3f14aa0bfb33459f91959e502e7fb063",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36",
        }
        datas = json.dumps(item)
        res = requests.post(url, data=datas, headers=headers)
        res.encoding = res.apparent_encoding
        if res.json()['message'] =='success':

            print('插入文章成功：{}'.format(item['title']))
        else:
            print(res.text)

