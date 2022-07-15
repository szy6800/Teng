# -*- coding: utf-8 -*-

# @Author : 石张毅
# @Site : https://www.chinabdc.cn/index.html#/NewHouse/list?prefix=20af0aa34818882190d7bb1af50832bc56e84ade4c52f6903294d957df939616dedb10bcdf22610c53331e74cb3411832f58245e57b7846f2ddf64c042841faa3d235c5cd938c92db3da804d2745fd2553121ec187645c30265e5d6b30343676
# @introduce: 青海住房平台 列表页数据
import hashlib
import json
import jsonpath
import scrapy
import copy
from urllib.parse import unquote

class HouseSpider(scrapy.Spider):
    name = 'house'
    # allowed_domains = ['chinabdc.cn']
    # start_urls = ['http://chinabdc.cn/']
    def __init__(self, *args, **kwargs):
        super(HouseSpider, self).__init__()

    def start_requests(self):
        for i in range(1000,1043):
            url = 'https://www.chinabdc.cn/Tool/Config/QueryMethodName?methodName=GetNHouseList&pageIndex={}&pageCount=10&filter_property=%7B%22mode%22:%22AND%22,%22data%22:[]%7D'.format(i)
            yield scrapy.Request(url, callback=self.parse)

    def parse(self, response, **kwargs):
        js_text = json.loads(response.text)
        # print(js_text)
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
        # 经度
        longitude = jsonpath.jsonpath(js_text,'$..longitude')
        # 维度
        latitude = jsonpath.jsonpath(js_text,'$..latitude')
        # 开发商
        developers = jsonpath.jsonpath(js_text,'$..developers')
        # 区县名
        disrictname = jsonpath.jsonpath(js_text,'$..disrictname')

        # deliverytime = jsonpath.jsonpath(js_text, '$..deliverytime')

        for id, name, house_type,area_range,nsale_time,address,features,price,lastmodifydate,longitude,latitude,developers,disrictname in \
                zip(url_id,name,house_type,area_range,nsale_time,address,features,price,lastmodifydate,longitude,latitude,developers,disrictname):
            item =dict()
            item['url'] = 'https://www.chinabdc.cn/index.html#/NewHouse/detail?ID='+id
            item['detail_id'] = id
            item['name'] = name
            item['house_type'] = house_type
            item['area_range'] = area_range
            item['nsale_time'] = nsale_time
            item['address'] = address
            # item['deliverytime'] = deliverytime
            item['features'] = features
            item['lng'] = longitude
            item['lat'] = latitude
            item['developers'] = developers

            item['disrictname'] = disrictname


            if price == 0.0:
                item['price'] = '价格待定'
            else:
                item['price'] = str(price) + '元/㎡起'
            item['lastmodifydate'] = lastmodifydate
            check_md5 = item['url']+item['name']
            item['check_md5'] = hashlib.md5(check_md5.encode(encoding='utf-8')).hexdigest()
            detail_url = 'https://www.chinabdc.cn/Tool/Config/QueryMethodName?methodName=GetProjectInfo&projectid='+item['detail_id']
            yield scrapy.Request(response.urljoin(detail_url), callback=self.parse_info, meta={'item': copy.deepcopy(item)},
                                 dont_filter=True)

    def parse_info(self,response):
        if response.status != 200:
            return
        item = response.meta['item']
        # 反序列化
        js_text = json.loads(response.text)
        # 单元楼名称
        try:
            units = jsonpath.jsonpath(js_text, '$..buildno..buildno')
            item['units'] = '|'.join(units)
        except:
            units = jsonpath.jsonpath(js_text, '$..buildno')
            item['units'] = units
        # # 总套数
        try:
            housecnt = jsonpath.jsonpath(js_text, '$..housecnt')[0]
            item['housecnt'] = '|'.join(housecnt)
        except:
            item['housecnt'] = ''
        # 可售数
        availablecnt = jsonpath.jsonpath(js_text, '$..availablecnt')[0]
        if availablecnt is None:
            item['availablecnt'] = ''
        else:
            item['availablecnt'] = str(availablecnt)
        # 已售数
        soldcnt = jsonpath.jsonpath(js_text, '$..soldcnt')[0]
        if soldcnt is None:
            item['soldcnt'] = ''
        else:
            item['soldcnt'] = str(soldcnt)
        # 不可售数
        unavailablecnt = jsonpath.jsonpath(js_text, '$..unavailablecnt')[0]
        if unavailablecnt is None:
            item['unavailablecnt'] = ''
        else:
            item['unavailablecnt'] = str(unavailablecnt)
        # 拟定合同数
        signcnt = jsonpath.jsonpath(js_text, '$..signcnt')[0]
        if signcnt is None:
            item['signcnt'] = ''
        else:
            item['signcnt'] = str(signcnt)
        # 销售名称
        item['salesname'] = jsonpath.jsonpath(js_text, '$..salesname')[0]

        # item['unavailablecnt'] = ''
        # item['signcnt'] = ''
        # item['availablecnt'] = ''
        # item['soldcnt'] = ''
        # item['salesname'] = ''
        yield item
















