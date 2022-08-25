# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import json

import requests

class LasaPipeline:
    def process_item(self, item, spider):
        #url = 'https://dev-api.yqypt.com/v2/policies/sync'
        #url = 'http://192.168.3.62:10010/policies/sync'
        url = 'https://api.yqypt.com/v2/policies/sync'
        token = "bfa89e563d9509fbc5c6503dd50faf2e"
        headers = {'content-type': 'application/json',
                   'syncToken': token}

        datas = json.dumps(item)
        res = requests.post(url, data=datas, headers=headers)
        res.encoding = res.apparent_encoding
        print('****************************************************')
        print(datas)
        print(res.text)
