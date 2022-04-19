# -*- coding: utf-8 -*-

# @Author : 石张毅
# @Site : https://www.chinabdc.cn/index.html#/NewHouse/list?prefix=20af0aa34818882190d7bb1af50832bc56e84ade4c52f6903294d957df939616dedb10bcdf22610c53331e74cb3411832f58245e57b7846f2ddf64c042841faa3d235c5cd938c92db3da804d2745fd2553121ec187645c30265e5d6b30343676
# @introduce: 青海住房平台 列表页数据
import hashlib
import json
import jsonpath
import scrapy


class HouseSpider(scrapy.Spider):
    name = 'house'
    # allowed_domains = ['chinabdc.cn']
    # start_urls = ['http://chinabdc.cn/']

    def start_requests(self):
        for i in range(100,104):
            url = 'https://www.chinabdc.cn/Tool/Config/QueryMethodName?methodName=GetNHouseList&pageIndex={}' \
                  '&pageCount=10&filter_property=%7B%22mode%22:%22AND%22,%22data%22:[]%7D'.format(i)
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response, **kwargs):
        js_text = json.loads(response.text)
        url_id = jsonpath.jsonpath(js_text,'$..id')
        # 小区名字
        name = jsonpath.jsonpath(js_text,'$..name')
        # 户型
        house_type = jsonpath.jsonpath(js_text,'$..housetyperange')
        # 面积范围
        area_range = jsonpath.jsonpath(js_text,'$..arearange')
        # 最新开盘日期
        nsale_time = jsonpath.jsonpath(js_text,'$..newestsaletime')
        # 地址
        address = jsonpath.jsonpath(js_text,'$..address')
        # 特征
        features = jsonpath.jsonpath(js_text,'$..projectfeatures')
        # 价格
        price = jsonpath.jsonpath(js_text,'$..startprice')
        # 价格更新日期
        lastmodifydate = jsonpath.jsonpath(js_text,'$..lastmodifydate')
        for id, name, house_type,area_range,nsale_time,address,features,price,lastmodifydate in zip(url_id,name,house_type,area_range,nsale_time,address,features,price,lastmodifydate):
            item = {}
            item['url'] = 'https://www.chinabdc.cn/index.html#/NewHouse/detail?ID='+id
            item['detail_id'] = id
            item['name'] = name
            item['house_type'] = house_type
            item['area_range'] = area_range
            item['nsale_time'] = nsale_time
            item['address'] = address
            item['features'] = features
            if price == 0.0:
                item['price'] = '价格待定'
            else:
                item['price'] = str(price) + '元/㎡起'
            item['lastmodifydate'] = lastmodifydate
            check_md5 = item['url']+item['name']
            item['check_md5'] = hashlib.md5(check_md5.encode(encoding='utf-8')).hexdigest()

            yield item





