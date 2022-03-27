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
    name = 'xinfang'

    def __init__(self, *args, **kwargs):
        super(XinfangSpider, self).__init__()
        # 南宁
        self.F = {
        }
        # 西安
        self.X = {
            # '高新': 'https://xian.newhouse.fang.com/house/s/gaoxin11/b96/',
            # '长安': 'https://xian.newhouse.fang.com/house/s/changan11/b92/',
            # '浐灞': 'https://xian.newhouse.fang.com/house/s/chanba21/b96/',
            # '经开': 'https://xian.newhouse.fang.com/house/s/jingkai11/b92/',
            # '西咸新区': 'https://xian.newhouse.fang.com/house/s/xixianxinqu/b910/',
            # '鄠邑': 'https://xi an.newhouse.fang.com/house/s/huyi/',
            # '高陵': 'https://xian.newhouse.fang.com/house/s/gaoling/b93/',
            # '临潼': 'https://xian.newhouse.fang.com/house/s/linchong/',
            # '蓝田': 'https://xian.newhouse.fang.com/house/s/lantian/b92/',
            # '周至': 'https://xian.newhouse.fang.com/house/s/zhouzhi/',
            # '城北': 'https://xian.newhouse.fang.com/house/s/chengbei11/b94/',
            # '城西': 'https://xian.newhouse.fang.com/house/s/chengxi11/b92/',
            # '城南': 'https://xian.newhouse.fang.com/house/s/chengnan11/b92/',
            '城东': 'https://xian.newhouse.fang.com/house/s/chengdong11/b92/',
            # '城内': 'https://xian.newhouse.fang.com/house/s/chengnei/',
            # '曲江': 'https://xian.newhouse.fang.com/house/s/qujiang1/b93/',
            # '周边': 'https://xian.newhouse.fang.com/house/s/zhoubian/',
            # '其他': 'https://xian.newhouse.fang.com/house/s/qita1/b95/'
        }
        self.result = dbz()

    def start_requests(self):
        for k, v in self.X.items():
            page = 1
            # print(v)
            # new_url = 'https://xian.newhouse.fang.com/house/s/'

            yield scrapy.Request(v, callback=self.parse, meta={'page': page, 'v' : v})

    def parse(self, response, *args, **kwargs):
        # print(response.text)
        page = response.meta['page']
        v = response.meta['v']
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
                # item['avg_price'] = counts['PROPERTYADDITION']
                # 物业类别
                item['operastion'] = counts['operastion']
                # 建筑物类别
                item['build_category'] = counts['buildCategory']
                # 产权年限
                item['right_desc'] = counts['right_desc']
                # 小区地址
                item['arch_add'] = counts['Address']
                # 开发商
                item['building_developers'] = counts['developerAll']
                # 占地面积
                item['covers_area'] = counts['GroundArea']
                # 建筑面积
                item['building_area'] = counts['PurposeArea']
                # 容积率
                item['plot_ratio'] = counts['Dimension']
                # 停车位
                item['parking_number'] = counts['ParkDesc']
                # 楼栋总数
                # item['building_number'] = counts['dongnum'] + '栋'
                # # 总户数
                item['house_number'] = counts['TotalDoor'] + '户'
                # 物业公司
                item['property_company'] = counts['manager']
                # 物业费
                item['property_fee'] = counts['property_fee']
                # 楼层数
                item['arch_floor'] = counts['BuildingDes']
                # 建筑年代
                item['building_time'] = ''
                # 主力户型面积
                item['main_door_area'] = ''
                # 单元数
                item['unit_number'] = ''
                # 人工是否核查
                item['verification'] = ''
                # 平均租金
                item['avg_rent'] = ''
                # 更新字段
                # item['update'] = counts['pricetype']
                # 网站中文名
                item['source_name'] = '房天下新房'
                # 网站来源
                item['source'] = ''
                # 入库时间
                item['crawler_time'] = str(datetime.datetime.now().strftime('%Y-%m-%d'))
                # # 数据详情链接
                # item['link'] = counts['domain']
                # 小区经度
                item['dispx'] = counts['baidu_coord_x']
                # 小区维度
                item['dispy'] = counts['baidu_coord_y']

                item['json_data'] = json.dumps(item, ensure_ascii=False)
                detail_urls = 'https://xian.newhouse.fang.com/loupan/'+id+'/housedetail.htm'
                # print(detail_urls)
                yield scrapy.Request(detail_urls, callback=self.parse_info, meta={'item': copy.deepcopy(item)}, dont_filter=True)
            # page += 1
            # friet_url = v + f'b9{str(page)}'
            # # print(friet_url)'https://xian.newhouse.fang.com/house/s/gaoling/
            # time.sleep(3)
            # yield scrapy.Request(friet_url, callback=self.parse, meta={'page': page})
        else:
            print('无房')
            return

    def parse_info(self,response):
        item = response.meta['item']
        # 数据详情链接
        item['link'] = response.url
        # 主力户型
        item['main_door'] = response.xpath("//*[contains(text(),'主力户型：')]/following::div[1]/a/text()").get()
        # 价格单位
        price_util = response.xpath('//*[@class="pricetd"]//em/text()').get()
        if price_util is None:
            item['avg_price'] = '暂无'
        else:
            item['avg_price'] = price_util
        # 楼栋总数
        building_number = response.xpath("//*[contains(text(),'楼栋总数：')]/following::div[1]/text()").get()
        if building_number is None:
            item['building_number'] = '暂无'
        else:
            item['building_number'] = building_number

        item['json_data'] = json.dumps(item, ensure_ascii=False)

        yield item








