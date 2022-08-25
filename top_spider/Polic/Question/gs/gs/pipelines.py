# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import json,requests
from openpyxl import Workbook

class GsPipeline(object):
    def process_item(self, item, spider):
        url = 'http://47.94.230.63:18080/policies/sync'
        # url = 'http://api.yqypt.com/policies/sync'
        headers = {'content-type': 'application/json',
                   'syncToken': 'bfa89e563d9509fbc5c6503dd50faf2e', }
        datas = json.dumps(item)
        res = requests.post(url, data=datas, headers=headers)
        res.encoding = res.apparent_encoding
        print('****************************************************')
        print(datas)
        print(res.text)





class ExcelPipeline(object):
    def __init__(self):
        self.wb = Workbook()
        self.ws = self.wb.active
        self.ws.append(['原文链接', '标题', '类型id', '答案正文', '正文标签'])
        self.file_name = "创业资讯.xlsx"

    def process_item(self, item, spider):
        line = [item['url'], item['title'], item['type_id'], item['answer'], item['answer_html']]
        self.ws.append(line)
        self.wb.save(self.file_name)
        return item

    def close_spider(self, spider):
        # 关闭
        self.wb.close()