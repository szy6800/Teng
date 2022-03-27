import datetime
import hashlib
import json

import scrapy
import re
import time
import requests
import copy

from copy import deepcopy
from sqlalchemy import create_engine
from loupan.items import LoupanItem
import numpy as np
import pandas as pd
# from loupan.tools.utils import Utils_

def md5_encrypt( chart):
    md = hashlib.md5(chart.encode())
    return md.hexdigest()

def dbz():
    # now = datetime.datetime.now()
    # otherStyleTime = now.strftime("%Y-%m-%d")

    sql1 = f'''SELECT id,county FROM `ershou` WHERE province='陕西省';'''
    sql2 = f'''SELECT id,county FROM `ershouid`;'''
    # print(sql)
    engine = create_engine('mysql+pymysql://root:123456@127.0.0.1:3306/ceshi?charset=utf8')
    engine2 = create_engine('mysql+pymysql://root:123456@127.0.0.1:3306/ceshi?charset=utf8')
    df = pd.read_sql(sql1, engine)
    df = df.drop_duplicates(subset=['id']) # 默认保留一条重复数据
    # print(df)
    df1 = pd.read_sql(sql2, engine2)
    df1 = df1.drop_duplicates(subset=['id'])  # 默认保留一条重复数据
    engine.dispose()
    engine2.dispose()
    # print(df1)
    db2 = pd.concat([df, df1], axis=0, sort=False, ignore_index=True)
    # print(db2)
    dbz = db2.drop_duplicates(subset=['id'], keep=False)
    # print(dbz)
    # print(f'对比保留了{len(dbz)}条')
    dbz = dbz[['id','county']].values.tolist() # df转列表
    # print(dbz)
    return dbz



class XinfangSpider(scrapy.Spider):
    name = 'xinfang2'
    # allowed_domains = ['www.c']
    # start_urls = ['http://www.c/']
    # custom_settings = {
    #     'COOKIES_ENABLED': 'False',
    #     'DEFAULT_REQUEST_HEADERS': {
    #         'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    #         'Accept-Language': 'en',
    #         "cookie": "global_cookie=zh70wkfvs63wvipbgt5286ivd1zl11qybub; __utmc=147"
    #                   "393320; token=c429b6983121480a8dab24ed95374b71; csrfToken=M18WzY_uymp"
    #                   "x8lp2-aZ8hGJF; city=xian; lastscanpage=0; __utma=147393320.102166071.16"
    #                   "47929978.1647929978.1647942782.2; __utmz=147393320.1647942782.2.2.utmcs"
    #                   "r=xian.esf.fang.com|utmccn=(referral)|utmcmd=referral|utmcct=/; g_so"
    #                   "urcepage=xf_lp%5Elpsy_pc; unique_cookie=U_zh70wkfvs63wvipbgt5286ivd1zl1"
    #                   "1qybub*117; __utmt_t0=1; __utmt_t1=1; __utmt_t2=1; __utmt_t3=1; __utmt"
    #                   "_t4=1; __utmb=147393320.49.10.1647942782",
    #         "origin": "https://xian.newhouse.fang.com",
    #         "user-agent": "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Triden"
    #                       "t/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0"
    #                       ".30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; LBBROWSER)"
    #     }
    # }

    def __init__(self, *args, **kwargs):
        super(XinfangSpider, self).__init__()
        self.result = dbz()

    def start_requests(self):
        count_list = self.result
        # print(count_list)
        x = 1
        item = {}
        for count in count_list[5599:5610]:
            # item = LoupanItem()
            # id = count[0]
            item["arch_id"] = count[0]

            # print(item["arch_id"])
            # item["arch_id"] ='3610205984'
            #区县
            item['country_name'] = count[1]
            if len(item['arch_id']) != 10:
                continue
            url = f'https://xian.newhouse.fang.com/loupan/{item["arch_id"]}/house/ajax/fixtiousPhoneGet/'
            cookies = "global_cookie=zh70wkfvs63wvipbgt5286ivd1zl11qybub; lastscanpage=0; city=www; resourceDetail=1; global_wapandm_cookie=osodt8ra6rq4bxhljv90pxdu51kl139970r; __utmc=147393320; csrfToken=D57SiLp0oF3Z821cDPqvKgnC; unique_wapandm_cookie=U_dxkpatvpvrig5ealebj4rdxrs12l17btzfg*1; g_sourcepage=xf_lp%5Elpsy_pc; __utma=147393320.102166071.1647929978.1648273622.1648280614.15; __utmz=147393320.1648280614.15.7.utmcsr=xian.esf.fang.com|utmccn=(referral)|utmcmd=referral|utmcct=/; __utmt_t0=1; unique_cookie=U_040m3ketvy4w948vuyhp95gd91tl17aorf7*40; __utmt_t1=1; __utmt_t2=1; __utmt_t3=1; __utmt_t4=1; __utmb=147393320.10.10.1648280614"
            cookies = {i.split('=')[0]: i.split('=')[1] for i in cookies.split('; ')}
            formdata = {
                'newcode': item["arch_id"],
                '_csrf': 'D57SiLp0oF3Z821cDPqvKgnC'
            }
            yield scrapy.FormRequest(url=url, formdata=formdata, callback=self.parse,meta={'item': copy.deepcopy(item)},
                                     dont_filter=True,
                                     cookies=cookies)


    def parse(self, response):
        item = response.meta['item']

        counts = json.loads(response.text)['data']

        item['uid'] = md5_encrypt(item['arch_id'])
        # 省份
        item['prov_name'] = '陕西省'
        # 地市
        item['city_name'] = '西安市'

        # arch_name 小区名称
        item['arch_name'] = counts['ProjName']

        # 物业类别
        item['operastion'] = counts['operastion']

        # 建筑物类别
        item['build_category'] = counts['buildCategory']
        # item['FixStatus'] = counts['FixStatus']
        # 产权年限
        item['right_desc'] = counts['right_desc']
        # item['Round_oracle'] = counts['Round_oracle']
        # 小区地址
        item['arch_add'] = counts['Address']
        # 开发商
        item['building_developers'] = counts['developerAll']
        # item['salestatus'] = counts['salestatus']
        # item['openhistory'] = counts['openhistory']['opentime']
        # item['livehistory'] = counts['livehistory']['livetime']
        # item['SaleAddress'] = counts['SaleAddress']
        # item['telephone'] = counts['telephone']
        # 占地面积
        item['covers_area'] = counts['GroundArea']
        # 建筑面积
        item['building_area'] = counts['PurposeArea']
        # 容积率
        item['plot_ratio'] = counts['Dimension']
        # item['VirescenceRate'] = counts['VirescenceRate']
        # 停车位
        item['parking_number'] = counts['ParkDesc']


        # 物业公司
        item['property_company'] = counts['manager']
        # 物业费
        item['property_fee'] = counts['property_fee']
        # 楼层数
        item['arch_floor'] = counts['BuildingDes']
        #item['ZONGFEN'] = counts['ZONGFEN']
        # 主力户型
        item['main_door'] = ''
        # 主力户型面积
        item['main_door_area'] = ''
        # 单元数
        item['unit_number'] = ''
        # 人工是否核查
        item['verification'] = ''
        # 平均租金
        item['avg_rent'] = ''

        # item['update'] = ''
        # 网站中文名
        item['source_name'] = '房天下'
        # 网站来源
        item['source'] = ''
        # 入库时间
        item['crawler_time'] = str(datetime.datetime.now().strftime('%Y-%m-%d'))
        # item['priceDateDesc'] = counts['priceDateDesc']
        # item['traffic'] = counts['traffic']
        # item['Layout'] = counts['Layout']
        # 小区经度
        item['dispx'] = counts['baidu_coord_x']
        # 小区维度
        item['dispy'] = counts['baidu_coord_y']

        # item['ProjDesc'] = counts['ProjDesc']
        # print(item)
        detail_urls = 'https://xian.esf.fang.com/loupan/'+item["arch_id"]+'.htm'
        # print(detail_urls)
        yield scrapy.Request(detail_urls, callback=self.parse_info, meta={'item': copy.deepcopy(item)},dont_filter=True)

    def parse_info(self,response):

        item = response.meta['item']
        # 数据详情链接
        item['link'] = response.url
        # 价格单位

        price_util = response.xpath('//*[@class="num_price"]/text()').get()
        if price_util is None:
            item['avg_price'] = '暂无'
        else:
            price = response.xpath('//*[@class="num_price"]/b/text()').get()
            item['avg_price'] = price+price_util
        # 楼栋总数
        building_number = response.xpath("//*[contains(text(),'楼栋总数')]/following::p[1]/text()").get()
        if building_number is None:
            item['building_number'] = '暂无'
        else:
            item['building_number'] = building_number
        # 总户数
        house_number = response.xpath("//*[contains(text(),'房屋总数')]/following::p[1]/text()").get()
        if house_number is None:
            item['house_number'] = '暂无'
        else:
            item['house_number'] = house_number
        # 建筑年代
        building_time = response.xpath("//*[contains(text(),'建筑年代')]/following::p[1]/text()").get()
        if building_time is None:
            item['building_time'] = '暂无'
        else:
            item['building_time'] = building_time

        item['json_data'] = json.dumps(item, ensure_ascii=False)

        yield item

