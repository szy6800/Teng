# -*- coding: utf-8 -*-

# @Time : 2022/3/22 16:30
# @Author : 石张毅
# @Site : 
# @File : test.py
# @Software: PyCharm 
import datetime
import hashlib
import json

import scrapy
import re
import time
import requests

from copy import deepcopy
from sqlalchemy import create_engine
# from loupan.items import LoupanItem
import numpy as np
import pandas as pd
# from loupan.tools.utils import Utils_

# import requests
# id = '3611057002'
# new_url = f'https://xian.newhouse.fang.com/loupan/{id}/house/ajax/fixtiousPhoneGet/'
# # print(new_url)
# payload = {
#     'newcode': id,
#     '_csrf': 'M18WzY_uympx8lp2-aZ8hGJF'
# }
#
# headers = {
#     'cookie': 'global_cookie=zh70wkfvs63wvipbgt5286ivd1zl11qybub; __utma=147393320.102166071.1647929978.1647929978.1647929978.1; __utmc=147393320; __utmz=147393320.1647929978.1.1.utmcsr=search.fang.com|utmccn=(referral)|utmcmd=referral|utmcct=/; city=; token=c429b6983121480a8dab24ed95374b71; csrfToken=M18WzY_uympx8lp2-aZ8hGJF; __utmt_t0=1; __utmt_t1=1; __utmt_t2=1; __utmt_t3=1; __utmt_t4=1; g_sourcepage=xf_lp%5Elpsy_pc; unique_cookie=U_zh70wkfvs63wvipbgt5286ivd1zl11qybub*76; __utmb=147393320.241.10.1647929978',
#     "origin": "https://xian.esf.fang.com",
#     "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36"
# }
#
# # print(id)
# respon = requests.post(url=new_url, headers=headers, data=payload)
# print(respon.json())



# def dbz():
#     # now = datetime.datetime.now()
#     # otherStyleTime = now.strftime("%Y-%m-%d")
#
#     sql1 = f'''SELECT arch_id,country_name FROM `arch_info_crawler` WHERE prov_name='陕西省';'''
#     sql2 = f'''SELECT id,county FROM `ershouid`;'''
#     # print(sql)
#     engine = create_engine('mysql+pymysql://root:123456@127.0.0.1:3306/ceshi?charset=utf8')
#     engine2 = create_engine('mysql+pymysql://root:123456@127.0.0.1:3306/ceshi?charset=utf8')
#     df = pd.read_sql(sql1, engine)
#     df = df.drop_duplicates(subset=['arch_id']) # 默认保留一条重复数据
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
#     print(f'对比保留了{len(dbz)}条')
#     dbz = dbz[['id','county']].values.tolist() # df转列表
#     print(len(dbz))
#     print(dbz)
#     return dbz
#
# dbz()

id = '3610192774'
new_url = f'https://xian.newhouse.fang.com/loupan/{id}/house/ajax/fixtiousPhoneGet/'
payload = {
    'newcode': id,
    '_csrf': 'M18WzY_uympx8lp2-aZ8hGJF'
}
headers = {
    "cookie": "global_cookie=zh70wkfvs63wvipbgt5286ivd1zl11qybub; __utmc=147393320; token=c429b6983121480a8dab24ed95374b71; csrfToken=M18WzY_uympx8lp2-aZ8hGJF; city=xian; lastscanpage=0; __utma=147393320.102166071.1647929978.1647929978.1647942782.2; __utmz=147393320.1647942782.2.2.utmcsr=xian.esf.fang.com|utmccn=(referral)|utmcmd=referral|utmcct=/; g_sourcepage=xf_lp%5Elpsy_pc; unique_cookie=U_zh70wkfvs63wvipbgt5286ivd1zl11qybub*117; __utmt_t0=1; __utmt_t1=1; __utmt_t2=1; __utmt_t3=1; __utmt_t4=1; __utmb=147393320.49.10.1647942782",
    "origin": "https://xian.newhouse.fang.com",
    "user-agent": "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; LBBROWSER)"
}
#             time.sleep(2)
respon = requests.post(url=new_url, headers=headers, data=payload)
print(respon.text)