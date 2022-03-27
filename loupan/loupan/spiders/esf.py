# -*- coding: utf-8 -*-

# @Author : 石张毅
# @Site :
# @introduce:

import hashlib
import json
import scrapy
import re
import time
import requests
from copy import deepcopy
from sqlalchemy import create_engine
import numpy as np
import pandas as pd
# from loupan.tools.utils import Utils_

# def md5_encrypt( chart):
#     md = hashlib.md5(chart.encode())
#     return md.hexdigest()
#
# def dbz():
#     # now = datetime.datetime.now()
#     # otherStyleTime = now.strftime("%Y-%m-%d")
#
#     sql1 = f'''SELECT id,county FROM `ershou` WHERE province='陕西省';'''
#     sql2 = f'''SELECT id,county FROM `ershouid`;'''
#     # print(sql)
#     engine = create_engine('mysql+pymysql://root:q!dwyyl6:q3L@127.0.0.1:3306/test?charset=utf8')
#     engine2 = create_engine('mysql+pymysql://root:q!dwyyl6:q3L@127.0.0.1:3306/test?charset=utf8')
#     df = pd.read_sql(sql1, engine)
#     df = df.drop_duplicates(subset=['id']) # 默认保留一条重复数据
#     # print(df)
#     df1 = pd.read_sql(sql2, engine2)
#     df1 = df1.drop_duplicates(subset=['id'])  # 默认保留一条重复数据
#     engine.dispose()
#     engine2.dispose()
#     # print(df1)
#     db2 = pd.concat([df, df1], axis=0, sort=False, ignore_index=True)
#     # print(db2)
#     dbz = db2.drop_duplicates(subset=['id'], keep=False)
#     # print(dbz)
#     # print(f'对比保留了{len(dbz)}条')
#     dbz = dbz[['id','county']].values.tolist() # df转列表
#     # print(dbz)
#     return dbz


class EsfSpider(scrapy.Spider):

    name = 'esf'

    headers = {
        #"cookie": "global_cookie=zh70wkfvs63wvipbgt5286ivd1zl11qybub; lastscanpage=0; resourceDetail=1; global_wapandm_cookie=osodt8ra6rq4bxhljv90pxdu51kl139970r; csrfToken=4O09MRRvc3qYKo5uv2ztXTKZ; __utmc=147393320; unique_wapandm_cookie=U_dxkpatvpvrig5ealebj4rdxrs12l17btzfg*1; city=xian; __utma=147393320.102166071.1647929978.1648280614.1648287268.16; __utmz=147393320.1648287268.16.8.utmcsr=xian.esf.fang.com|utmccn=(referral)|utmcmd=referral|utmcct=/loupan/3610191248.htm; g_sourcepage=esf_xq%5Elb_pc; __utmt_t0=1; __utmt_t1=1; __utmt_t2=1; unique_cookie=U_040m3ketvy4w948vuyhp95gd91tl17aorf7*46; __utmb=147393320.24.10.1648287268",
        "referer": "https://xian.esf.fang.com/housing/__0_3_0_0_2_0_0_0/?rfss=1-1f9d8ac6c51244a123-08",
        "user-agent": "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; LBBROWSER)"
    }
    def __init__(self, *args, **kwargs):
        super(EsfSpider, self).__init__()
    def start_requests(self):
        # 二手房所有列表页链接
        urls = ['https://xian.esf.fang.com/housing/__0_3_0_0_{}_0_0_0/'.format(i) for i in range(1, 2)]
        for url in urls:
            cookies = 'global_cookie=zh70wkfvs63wvipbgt5286ivd1zl11qybub; lastscanpage=0; resourceDetail=1; global_wapandm_cookie=osodt8ra6rq4bxhljv90pxdu51kl139970r; csrfToken=4O09MRRvc3qYKo5uv2ztXTKZ; __utmc=147393320; unique_wapandm_cookie=U_dxkpatvpvrig5ealebj4rdxrs12l17btzfg*1; city=xian; __utma=147393320.102166071.1647929978.1648280614.1648287268.16; __utmz=147393320.1648287268.16.8.utmcsr=xian.esf.fang.com|utmccn=(referral)|utmcmd=referral|utmcct=/loupan/3610191248.htm; g_sourcepage=esf_xq^lb_pc; __utmt_t0=1; __utmt_t1=1; __utmt_t2=1; unique_cookie=U_040m3ketvy4w948vuyhp95gd91tl17aorf7*46; __utmb=147393320.24.10.1648287268'
            cookies = {i.split('=')[0]: i.split('=')[1] for i in cookies.split('; ')}
            # print(cookies)
            yield scrapy.Request(url=url, callback=self.parse, cookies=cookies,
                                 headers=self.headers)

    def parse(self, response, *args, **kwargs):
        item = {}
        # 详情页链接
        content_list = response.xpath('//*[@class="plotTit"]/@href').getall()
        # 小区名称
        arch_name = response.xpath('//*[@class="plotTit"]/text()').getall()
        print(arch_name, content_list)



