# 采集器

import hashlib
from datetime import datetime, date, timedelta
import scrapy
import datetime
import pymysql
from yushou.uredis import Redis_DB
from sqlalchemy import create_engine
import pymysql
from sqlalchemy.types import *
import numpy as np
import pandas as pd


def queryue(sql):
    engine = create_engine('mysql+pymysql://root:Lxp.138927!asd@123.126.87.123:3306/crawler2022?charset=utf8')
    # engine = create_engine('mysql+pymysql://root:123456@127.0.0.1:3306/ceshi?charset=utf8',)
    df = pd.read_sql_query(sql, engine)
    lists1 = np.array(df)
    lists = lists1.tolist()
    # print(lists)
    return lists


def md5_encrypt(chart):
    # MD5 加密
    md = hashlib.md5(chart.encode())
    return md.hexdigest()


def id_sult():
    now = datetime.datetime.utcnow()
    otherStyleTime = now.strftime("%Y-%m-%d")
    yesterday = date.today() + timedelta(days=-1)
    sql = f"SELECT uid,uuid,title,link,intro,abs,content,publish_time,purchaser,proxy,create_time,update_time,deleted,province,base,type,items,data_source,end_time,status,serial FROM `caijiqi` where date(create_time)=curdate()"
    # sql = f"SELECT uid,uuid,title,link,intro,abs,content,publish_time,purchaser,proxy,create_time,update_time,deleted,province,base,type,items,data_source,end_time,status,serial FROM `caijiqi` where date(create_time)=date_sub(curdate(),interval 2 day)"
    # sql = f"SELECT uid,uuid,title,link,intro,abs,content,publish_time,purchaser,proxy,create_time,update_time,deleted,province,base,type,items,data_source,end_time,status,serial FROM `caijiqi` where data_source='00664' and  date(create_time)=curdate();"
    # sql = f"SELECT uid,uuid,title,link,intro,abs,content,publish_time,purchaser,proxy,create_time,update_time,deleted,province,base,type,items,data_source,end_time,status,serial FROM `caijiqi` where data_source='00664' and date(create_time)=date_sub(curdate(),interval 1 day);"
    result1 = queryue(sql=sql)
    # print(result1)
    page = len(result1)
    print(f'========读取总数>>{page}条=======')
    # print(result1)
    # print(result1)
    result = []
    nows = datetime.datetime.now()
    otherStyleTimes = nows.strftime("%Y-%m-%d")
    for i in range(len(result1)):
        result1[i][0] = md5_encrypt(result1[i][2]+result1[i][3]+result1[i][7])
        result1[i][10] = otherStyleTimes
        result.append(result1[i])
    # for i in range(page):
    #     # print(result1)
    #     # result1[i][0] = result1[i][0].replace('http:','https:')
    #     # result1[i][2] = result1[i][2].replace('http:','https:')
    #     # result1[i][4] = result1[i][4].replace('http:','https:')
    #     # print(result1[i][1:])
    #     result.append(result1[i][1:])
    print('=========读取完毕=========')
    return result


class XukeSpider(scrapy.Spider):
    name = 'xuke'
    # allowed_domains = ['www']
    start_urls = ['https://www.jd.com/']

    def __init__(self, *args, **kwargs):
        super(XukeSpider, self).__init__()
        self.result = id_sult()

    def start_requests(self):
        resultc = id_sult()
        # print(resultc)
        new_url = 'https://www.suning.com/'
        yield scrapy.Request(new_url, callback=self.parse,meta={"resultc": resultc})

    def parse(self, response, *args, **kwargs):
        # print(resultc)
        for res in self.result:
            item = {}
            item['uid'] = res[0]
            if Redis_DB().Redis_pd(item['uid']) is True:  # 数据去重
                print(item['uid'], '\033[0;35m <=======此数据已采集=======> \033[0m')
                continue
            item['uuid'] = res[1]
            item['title'] = res[2]
            item['link'] = res[3]
            item['intro'] = res[4]
            item['abs'] = res[5]
            item['content'] = res[6]
            item['publish_time'] = res[7]
            item['purchaser'] = res[8]
            item['proxy'] = res[9]
            item['create_time'] = res[10]
            item['update_time'] = res[11]
            item['deleted'] = res[12]
            item['province'] = res[13]
            item['base'] = res[14]
            item['type'] = res[15]
            item['items'] = res[16]
            item['data_source'] = res[17]
            item['end_time'] = res[18]
            item['status'] = res[19]
            item['serial'] = res[20]
            yield item

