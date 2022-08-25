# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import requests
import json
import pymysql


class HefeiPipeline(object):

    def process_item(self, item, spider):
        url = 'http://api.yqypt.com/v2/policies/sync'
        token = "bfa89e563d9509fbc5c6503dd50faf2e"
        headers = {'content-type': 'application/json',
                   'syncToken': token}
        datas = json.dumps(item)
        res = requests.post(url, data=datas, headers=headers)
        res.encoding = res.apparent_encoding
        print('****************************************************')
        print(datas)
        print(res.text)


class AndroidPipeline(object):

    def __init__(self):
        dbparams = {
            'host': '47.94.230.63',
            'port': 13306,
            'user': 'root',
            'password': 'Yqy@1234',
            'database': 'ssc'
        }
        self.conn = pymysql.connect(**dbparams)
        self.cursor = self.conn.cursor()
        self._sql = None

    def process_item(self, item, spider):
        self.cursor.execute(self.sql, (item['contentUrl'], item['coverImgUrl'], item['articleTitle'],item['articleDesc'],item['contentHtml'],item['type']))
        self.conn.commit()
        return item

    @property
    def sql(self):
        if not self._sql:
            self._sql = """
            insert into convioud(id,contentUrl,coverImgUrl,articleTitle,articleDesc,contentHtml,type) values (null,%s,%s,%s,%s,%s,%s)

            """
            return self._sql
        return self._sql