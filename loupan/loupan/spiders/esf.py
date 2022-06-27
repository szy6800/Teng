# -*- coding: utf-8 -*-

# @Author : 石张毅
# @Site :
# @introduce:
import copy
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
def dbz():
    # now = datetime.datetime.now()
    # otherStyleTime = now.strftime("%Y-%m-%d")

    sql1 = f'''SELECT id,county FROM `ershou` WHERE province='陕西省';'''
    sql2 = f'''SELECT id,county FROM `ershou_copy1`;'''
    # print(sql)
    engine = create_engine('mysql+pymysql://root:123456@127.0.0.1:3306/test?charset=utf8')
    engine2 = create_engine('mysql+pymysql://root:123456@127.0.0.1:3306/test?charset=utf8')
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


class EsfSpider(scrapy.Spider):

    name = 'esf'

    headers = {
        'referer': 'https://xian.esf.fang.com/housing/',
        "user-agent": "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; LBBROWSER)"
    }
    def __init__(self, *args, **kwargs):
        super(EsfSpider, self).__init__()
        self.result = dbz()

    def start_requests(self):
        cookies = 'global_cookie=6yo0tgoczsr0ran9bqmbsunjk17l4wgco0c; __utmc=147393320; __utma=147393320.941139512.1656316964.1656316964.1656320591.2; __utmz=147393320.1656320591.2.2.utmcsr=xian.esf.fang.com|utmccn=(referral)|utmcmd=referral|utmcct=/housing/; __utmt_t0=1; __utmt_t1=1; __utmt_t2=1; city=www1; csrfToken=R99ggL-QWVP4n-LfcObF2Ctz; unique_cookie=U_6yo0tgoczsr0ran9bqmbsunjk17l4wgco0c*51; g_sourcepage=; __utmb=147393320.91.10.1656320591'
        cookies = {i.split('=')[0]: i.split('=')[1] for i in cookies.split('; ')}
        # 二手房所有列表页链接
        for i in self.result[700:800]:
            url = 'https://xianyang.esf.fang.com/loupan/{}.htm'.format(i[0])
            # print(cookies)
            item=dict()
            item['id'] = i[0]
            yield scrapy.Request(url=url, callback=self.parse, cookies=cookies,headers=self.headers,
                                 dont_filter=True,meta={'item': copy.deepcopy(item)})

    def parse(self, response, *args, **kwargs):
        # 套數
        item = response.meta['item']
        item['esf_count'] = response.xpath("//*[@id='kesfxqxq_A01_01_02']/p/a/text()").get()
        # 價格
        item['price'] = response.xpath('//*[@class="num_price"]/b/text()').get()+'元/㎡'
        yield item



