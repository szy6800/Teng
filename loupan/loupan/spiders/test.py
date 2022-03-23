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
# from loupan.items import LoupanItem
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
    name = 'test'

    def __init__(self, *args, **kwargs):
        super(XinfangSpider, self).__init__()
        # 南宁
        self.F = {

        }
        # 西安
        self.X = {
            '高新': 'https://xian.newhouse.fang.com/house/s/gaoxin11/',
            # '长安': 'https://xian.newhouse.fang.com/house/s/changan11/',
            # '浐灞': 'https://xian.newhouse.fang.com/house/s/chanba21/',
            # '经开': 'https://xian.newhouse.fang.com/house/s/jingkai11/',
            # '西咸新区': 'https://xian.newhouse.fang.com/house/s/xixianxinqu/',
            # '鄠邑': 'https://xian.newhouse.fang.com/house/s/huyi/',
            # '高陵': 'https://xian.newhouse.fang.com/house/s/gaoling/',
            # '临潼': 'https://xian.newhouse.fang.com/house/s/linchong/',
            # '蓝田': 'https://xian.newhouse.fang.com/house/s/lantian/',
            # '周至': 'https://xian.newhouse.fang.com/house/s/zhouzhi/',
            # '城北': 'https://xian.newhouse.fang.com/house/s/chengbei11/',
            # '城西': 'https://xian.newhouse.fang.com/house/s/chengxi11/',
            # '城南': 'https://xian.newhouse.fang.com/house/s/chengnan11/',
            # '城东': 'https://xian.newhouse.fang.com/house/s/chengdong11/',
            # '城内': 'https://xian.newhouse.fang.com/house/s/chengnei/',
            # '曲江': 'https://xian.newhouse.fang.com/house/s/qujiang1/',
            # '周边': 'https://xian.newhouse.fang.com/house/s/zhoubian/',
            # '其他': 'https://xian.newhouse.fang.com/house/s/qita1/'
        }
        self.result = dbz()

    def start_requests(self):
        for k, v in self.X.items():
            page = 1
            # print(v)
            # new_url = 'https://xian.newhouse.fang.com/house/s/'

            yield scrapy.Request(v, callback=self.parse, meta={'page': page})

    def parse(self, response):
        # print(response.text)
        page = response.meta['page']
        if response.xpath('//h4[@class="f18"]/text()').get() == None:
            count_list = response.xpath('//div[@class="nlcd_name"]/a')
            for count in count_list:
                url = count.xpath('./@href').get()
                # print(url)
                id = re.search('loupan/(.*?).htm', url).group(1)
                # print(id)
                new_url = f'https://xian.newhouse.fang.com/loupan/{id}/house/ajax/fixtiousPhoneGet/'
                payload = {
                    'newcode': id,
                    '_csrf': 'M18WzY_uympx8lp2-aZ8hGJF'
                }
                headers = {
                    "cookie": "global_cookie=zh70wkfvs63wvipbgt5286ivd1zl11qybub; __utmc=147393320; token=c429b6983121480a8dab24ed95374b71; csrfToken=M18WzY_uympx8lp2-aZ8hGJF; city=xian; lastscanpage=0; __utma=147393320.102166071.1647929978.1647929978.1647942782.2; __utmz=147393320.1647942782.2.2.utmcsr=xian.esf.fang.com|utmccn=(referral)|utmcmd=referral|utmcct=/; g_sourcepage=xf_lp%5Elpsy_pc; unique_cookie=U_zh70wkfvs63wvipbgt5286ivd1zl11qybub*117; __utmt_t0=1; __utmt_t1=1; __utmt_t2=1; __utmt_t3=1; __utmt_t4=1; __utmb=147393320.49.10.1647942782",
                    "origin": "https://xian.newhouse.fang.com",
                    "user-agent": "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; LBBROWSER)",
                    "sec-fetch-dest": "empty",
                    "sec-fetch-mode": "cors",
                    "sec-fetch-site": "same-origin",
                    "x-requested-with": "XMLHttpRequest",
                }
    #             time.sleep(2)
                respon = requests.post(url=new_url, headers=headers, data=payload)
                # print(respon.text)
                item = {}
                counts = json.loads(respon.text)['data']
                item['uid'] = md5_encrypt(id)

                item['arch_id'] = id
                # 省份
                item['prov_name'] = '陕西省'
                # 地市
                item['city_name'] = '西安市'
                # 区县
                item['country_name'] = '不限'
                # arch_name 小区名称
                item['arch_name'] = counts['ProjName']
                # avg_price
                item['avg_price'] = counts['PROPERTYADDITION']
                # 物业类别
                item['operastion'] = counts['operastion']
                #item['house_feature'] = counts['house_feature']
                # 建筑物类别
                item['build_category'] = counts['buildCategory']
                #item['FixStatus'] = counts['FixStatus']
                # 产权年限
                item['right_desc'] = counts['right_desc']
                #item['Round_oracle'] = counts['Round_oracle']
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
                # 楼栋总数
                item['building_number'] = counts['dongnum'] + '栋'
                # 总户数
                item['house_number'] = counts['TotalDoor'] + '户'
                # 物业公司
                item['property_company'] = counts['manager']
                # 物业费
                item['property_fee'] = counts['property_fee']
                # 楼层数
                item['arch_floor'] = counts['BuildingDes']
                #item['ZONGFEN'] = counts['ZONGFEN']
                # # 平均房价(元/㎡)
                # item['price'] = counts['price']
                # 建筑年代
                item['building_time'] = ''
                # 主力户型
                item['main_door'] = ''
                # 主力户型面积
                item['main_door_area'] = ''
                # 单元数
                item['unit_number'] = ''
                # 人工是否核查
                item['verification'] = ''
                # 平均租金
                item['avg_rent'] = counts['pricetype']
                # 更新字段
                # item['update'] = counts['pricetype']
                # 网站中文名
                item['source_name'] = '房天下新房'
                # 网站来源
                item['source'] = ''
                # 入库时间
                item['crawler_time'] = ''
                # 数据详情链接
                item['link'] = counts['domain']

                # item['priceDateDesc'] = counts['priceDateDesc']
                # item['traffic'] = counts['traffic']
                # item['Layout'] = counts['Layout']
                # 小区经度
                item['dispx'] = counts['baidu_coord_x']
                # 小区维度
                item['dispy'] = counts['baidu_coord_y']

                item['json_data'] = json.dumps(item, ensure_ascii=False)
                # item['ProjDesc'] = counts['ProjDesc']
                # print(item)

                yield item

            page += 1
            friet_url = 'https://xian.newhouse.fang.com/house/s/' + f'b9{str(page)}'
            print(friet_url)
            time.sleep(3)
            yield scrapy.Request(friet_url, callback=self.parse, meta={'page': page})

        else:
            print('无房')
            return

    # def start_requests(self):
    #     count_list = self.result
    #
    #     # print(count_list)
    #     x = 1
    #     item = {}
    #     for count in count_list:
    #         # item = LoupanItem()
    #         # id = count[0]
    #         item["id"] = count[0]
    #         # 区县
    #         item['country_name'] = count[1]
    #         # item["id"] = '3610192608'
    #         if len(item['id']) != 10:
    #             continue
    #         url = f'https://xian.newhouse.fang.com/loupan/{item["id"]}/house/ajax/fixtiousPhoneGet/'
    #         formdata = {
    #             'newcode': item["id"],
    #             '_csrf': 'M18WzY_uympx8lp2-aZ8hGJF'
    #         }
    #         yield scrapy.FormRequest(url=url, formdata=formdata, callback=self.parse,meta={'item': copy.deepcopy(item)})
    #
    #
    # def parse(self, response):
    #     item = response.meta['item']
    #     # print(response.text)
    #     counts = json.loads(response.text)['data']
    #
    #     item['uid'] = md5_encrypt(item['id'])
    #     # 省份
    #     item['prov_name'] = '陕西省'
    #     # 地市
    #     item['city_name'] = '西安市'
    #
    #     # arch_name 小区名称
    #     item['arch_name'] = counts['ProjName']
    #     # avg_price
    #     item['avg_price'] = counts['PROPERTYADDITION']
    #     # 物业类别
    #     item['operastion'] = counts['operastion']
    #     item['house_feature'] = counts['house_feature']
    #     # 建筑物类别
    #     item['build_category'] = counts['buildCategory']
    #     item['FixStatus'] = counts['FixStatus']
    #     # 产权年限
    #     item['right_desc'] = counts['right_desc']
    #     item['Round_oracle'] = counts['Round_oracle']
    #     # 小区地址
    #     item['arch_add'] = counts['Address']
    #     # 开发商
    #     item['building_developers'] = counts['developerAll']
    #     # item['salestatus'] = counts['salestatus']
    #     # item['openhistory'] = counts['openhistory']['opentime']
    #     # item['livehistory'] = counts['livehistory']['livetime']
    #     # item['SaleAddress'] = counts['SaleAddress']
    #     # item['telephone'] = counts['telephone']
    #     # 占地面积
    #     item['covers_area'] = counts['GroundArea']
    #     # 建筑面积
    #     item['building_area'] = counts['PurposeArea']
    #     # 容积率
    #     item['plot_ratio'] = counts['Dimension']
    #     # item['VirescenceRate'] = counts['VirescenceRate']
    #     # 停车位
    #     item['parking_number'] = counts['ParkDesc']
    #     # 楼栋总数
    #     item['building_number'] = counts['dongnum'] + '栋'
    #     # 总户数
    #     item['house_number'] = counts['TotalDoor'] + '户'
    #     # 物业公司
    #     item['property_company'] = counts['manager']
    #     # 物业费
    #     item['property_fee'] = counts['property_fee']
    #     # 楼层数
    #     item['arch_floor'] = counts['BuildingDes']
    #     #item['ZONGFEN'] = counts['ZONGFEN']
    #     # 平均房价(元/㎡)
    #     item['price'] = counts['price']
    #     # 建筑年代
    #     item['building_time'] = ''
    #     # 主力户型
    #     item['main_door'] = ''
    #     # 主力户型面积
    #     item['main_door_area'] = ''
    #     # 单元数
    #     item['unit_number'] = ''
    #     # 人工是否核查
    #     item['verification'] = ''
    #     # 平均祖新
    #     item['avg_rent'] = counts['pricetype']
    #     # 更新字段
    #     item['update'] = counts['pricetype']
    #     # 网站中文名
    #     item['source_name'] = ''
    #     # 网站来源
    #     item['source'] = ''
    #     # 入库时间
    #     item['crawler_time'] = ''
    #     # 数据详情链接
    #     item['link'] = counts['domain']
    #
    #     # item['priceDateDesc'] = counts['priceDateDesc']
    #     # item['traffic'] = counts['traffic']
    #     # item['Layout'] = counts['Layout']
    #     # 小区经度
    #     item['dispx'] = counts['baidu_coord_x']
    #     # 小区维度
    #     item['lat'] = counts['baidu_coord_y']
    #
    #     item['json_data'] = json.dumps(item, ensure_ascii=False)
    #     # item['ProjDesc'] = counts['ProjDesc']
    #     # print(item)
    #     yield item







