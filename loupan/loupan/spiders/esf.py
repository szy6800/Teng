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

    def __init__(self, *args, **kwargs):
        super(EsfSpider, self).__init__()
        # self.result = dbz()

    def start_requests(self):
        # 二手房所有列表页链接
        urls = ['https://xian.esf.fang.com/housing/__0_3_0_0_{}_0_0_0/'.format(i) for i in range(1, 4)]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        item = {}
        # 详情页链接
        content_list = response.xpath('//*[@class="plotTit"]/@href').getall()
        # 小区名称
        arch_name = response.xpath('//*[@class="plotTit"]/text()').getall()
        print(arch_name, content_list)



