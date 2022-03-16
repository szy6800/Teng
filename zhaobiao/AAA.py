import datetime
import os
import time
import datetime
import pymysql
from sqlalchemy import create_engine
import pymysql
from apscheduler.schedulers.blocking import BlockingScheduler
from sqlalchemy.types import *
import numpy as np
import pandas as pd


def dbz(count):
    # now = datetime.datetime.now()
    # otherStyleTime = now.strftime("%Y-%m-%d")

    sql1 = f'''SELECT id,url,link,title,county FROM `dianping2021` WHERE county='{count}';'''
    sql2 = f'''SELECT id,url,link,title,county FROM `dianping2021_pro` WHERE county='{count}';'''
    #print(sql1)
    engine = create_engine('mysql+pymysql://root:123456@127.0.0.1:3306/ceshi?charset=utf8')
    engine2 = create_engine('mysql+pymysql://root:123456@127.0.0.1:3306/ceshi?charset=utf8')
    df = pd.read_sql(sql1, engine)
    df = df.drop_duplicates(subset=['id'])  # 默认保留一条重复数据
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
    print(f'对比保留了{len(dbz)}条')
    dbz = dbz[['id', 'url', 'link', 'title', 'county']].values.tolist()  # df转列表
    # print(dbz)
    return dbz

print(dbz('碑林区'))