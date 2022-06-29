import datetime
import redis
import random
from sqlalchemy import create_engine
from apscheduler.schedulers.blocking import BlockingScheduler
import numpy as np
import pandas as pd
import requests

def queryue(sql):
    engine = create_engine('mysql+pymysql://root:Lxp.138927!asd@123.126.87.123:3306/crawler2022?charset=utf8')
    # engine = create_engine('mysql+pymysql://root:Zfw3aVMkb^KVew6q@123.126.87.125:3306/crawler2022?charset=utf8')

    df = pd.read_sql_query(sql, engine)

    lists1 = np.array(df)

    lists = lists1.tolist()
    # print(lists)
    return lists

# 模糊查询
"""SELECT * FROM meituan2 WHERE url LIKE '%fz.meituan.com%';"""


def id_sult():
    # sql = 'SELECT * FROM meituan1 WHERE 地市详情链接="http://nd.meituan.com/meishi"'
    # sql = 'SELECT * FROM zhaobiao2021;'
    sql = f"SELECT uid FROM `zhaobiao2021` WHERE create_time='2022-06-28';"
    result1 = queryue(sql=sql)
    page = len(result1)
    print(f'========读取总数>>{page}条=======')
    # print(result1)
    # print(result1)
    result = []
    for i in range(page):
        # print(1)
        # result1[i][0] = result1[i][0].replace('http:','https:')
        # result1[i][2] = result1[i][2].replace('http:','https:')
        # result1[i][4] = result1[i][4].replace('http:','https:')
        # print(result1[i][1:])
        result.append(result1[i][0])
    print('=========读取完毕=========')
    return result


class Redis_Ip():

    def __init__(self):
        self.pool2 = redis.ConnectionPool(
            host='123.56.87.41', port=6379, password='$SMe9ndaZQw$4bJ2', decode_responses=True
        )
        self.db2 = redis.Redis(connection_pool=self.pool2)
        # 获取所有ip返回列表
        self.result = id_sult()


    def start(self):
        page = 1
        for i in self.result:
            self.db2.hset('bulongquchong', i,'')
            print(page)
            page+=1

Redis_Ip().start()
