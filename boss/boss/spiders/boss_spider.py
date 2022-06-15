# -*- coding: utf-8 -*-

# @Author : 石张毅
# @Site : https://www.zhipin.com/
# @introduce: 所有岗位信息

import scrapy
import json
import jsonpath


class BossSpiderSpider(scrapy.Spider):
    name = 'boss_spider'
    # allowed_domains = ['boss.com']

    def __init__(self, *args, **kwargs):
        super(BossSpiderSpider, self).__init__()

    def start_requests(self):
        url = 'https://www.zhipin.com/wapi/zpCommon/data/position.json'
        yield scrapy.Request(url, callback=self.parse)

    def parse(self, response, *args, **kwargs):

        js_text = json.loads(response.text)
        # item['big_type'] = jsonpath.jsonpath(js_text,'$..zpData.tip')
        big_type = js_text['zpData']

        for big in big_type:
            item = dict()
            # 岗位大分类
            item['big_type'] = big['name']
            item['big_code'] = big['code']
            mid_type = big['subLevelModelList']
            # 中级岗位
            for mid in mid_type:
                item['mid_type'] = mid['name']
                item['mid_code'] = mid['code']
                small_type = mid['subLevelModelList']
                # 岗位小分类
                for small in small_type:
                    item['small_type'] = small['name']
                    item['small_code'] = small['code']
                    yield item


