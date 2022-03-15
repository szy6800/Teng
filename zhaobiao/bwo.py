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


def queryue(sql):
    engine = create_engine('mysql+pymysql://root:I0z>kp9tnavw@123.56.87.41:3306/crawler2021?charset=utf8')
    # engine = create_engine('mysql+mysqlconnector://root:@127.0.0.1:3306/test?charset=utf8')

    df = pd.read_sql_query(sql, engine)

    lists1 = np.array(df)

    lists = lists1.tolist()
    # print(lists)
    return lists

# 模糊查询
"""SELECT * FROM meituan2 WHERE url LIKE '%fz.meituan.com%';"""


def id_sult():
    sql = "SELECT * FROM `zhaobiao2021` WHERE create_time='2021-09-29';"
    result1 = queryue(sql=sql)

    result = []
    for i in range(len(result1)):
        result.append(result1[i][1:])
    return result


def df_to_mysql(df):
    df.to_sql(name = 'zhaobiao2021',
            con = 'mysql+pymysql://root:@127.0.0.1:3306/test?charset=utf8',
            # con = 'mysql+pymysql://root:I0z>kp9tnavw@123.56.87.41:3306/crawler2021?charset=utf8',
            if_exists = 'append',index=False,
    chunksize=20000)


def dbz():
    now = datetime.datetime.now()
    otherStyleTime = now.strftime("%Y-%m-%d")

    sql = f'''SELECT uid,uuid,title,link,intro,abs,content,publish_time,purchaser,proxy,create_time,update_time,deleted,province,base,type,items,data_source,end_time,status,serial FROM `zhaobiao2021` WHERE create_time='{otherStyleTime}' AND data_source!='00108';'''
    # sql = f'''SELECT uid,uuid,title,link,intro,abs,content,publish_time,purchaser,proxy,create_time,update_time,deleted,province,base,type,items,data_source,end_time,status,serial FROM `zhaobiao2021` WHERE create_time>'2022-02-01' AND data_source!='00108';'''
    # sql = '''SELECT uid,uuid,title,link,intro,abs,content,publish_time,purchaser,proxy,create_time,update_time,deleted,province,base,type,items,data_source,end_time,status,serial FROM `zhaobiao2021` WHERE create_time='2021-10-19';'''
    # pymysql
    engine = create_engine('mysql+pymysql://root:@127.0.0.1:3306/test?charset=utf8')
    engine2 = create_engine('mysql+pymysql://root:I0z>kp9tnavw@123.56.87.41:3306/crawler2021?charset=utf8')
    df = pd.read_sql(sql, engine)
    # print(df)
    df1 = pd.read_sql(sql, engine2)
    engine.dispose()
    engine2.dispose()
    # print(df1)
    db2 = pd.concat([df, df1], axis=0, sort=False, ignore_index=True)
    # print(db2)
    dbz = db2.drop_duplicates(subset=['uid'], keep=False)
    # print(dbz)
    print(f'对比保留了{len(dbz)}条')
    return dbz


def job():
    start_times = datetime.datetime.now()  # 采集开始时间
    start_time = str(start_times).split('.')[0]
    print('Starting time ===>', start_time)

    # 采集逻辑
    print('Bidding website data transfer =============>crawler2021.zhaobiao2021!!!!')
    '''
    入库程序
    '''

    db3 = dbz()

    if len(db3) > 0:
        df_to_mysql(db3)
        print('入库完毕')
    else:
        print('无数据')


    print('Collect again after 1 hour!!!!')

    end_time = str(datetime.datetime.now()).split('.')[0]  # 采集结束时间
    print(f"Starting time ===> {start_time}, End time ===> {end_time}")
    next_start_time = (start_times + datetime.timedelta(days=1)).strftime('%Y/%m/%d %H:%M:%S')  # 下次采集间隔时间
    print('Next startup time =====>', next_start_time, '\n')

# def dbz(otherStyleTime):
#     # now = datetime.datetime.now()
#     # otherStyleTime = now.strftime("%Y-%m-%d")
#
#     sql = f'''SELECT uid,uuid,title,link,intro,abs,content,publish_time,purchaser,proxy,create_time,update_time,deleted,province,base,type,items,data_source,end_time,status,serial FROM `zhaobiao2021` WHERE create_time='{otherStyleTime}' AND data_source!='00108';'''
#     # sql = f'''SELECT uid,uuid,title,link,intro,abs,content,publish_time,purchaser,proxy,create_time,update_time,deleted,province,base,type,items,data_source,end_time,status,serial FROM `zhaobiao2021` WHERE create_time>'2022-02-01' AND data_source!='00108';'''
#     # sql = '''SELECT uid,uuid,title,link,intro,abs,content,publish_time,purchaser,proxy,create_time,update_time,deleted,province,base,type,items,data_source,end_time,status,serial FROM `zhaobiao2021` WHERE create_time='2021-10-19';'''
#     # pymysql
#     engine = create_engine('mysql+pymysql://root:@127.0.0.1:3306/test?charset=utf8')
#     engine2 = create_engine('mysql+pymysql://root:I0z>kp9tnavw@123.56.87.41:3306/crawler2021?charset=utf8')
#     df = pd.read_sql(sql, engine)
#     # print(df)
#     df1 = pd.read_sql(sql, engine2)
#     engine.dispose()
#     engine2.dispose()
#     # print(df1)
#     db2 = pd.concat([df, df1], axis=0, sort=False, ignore_index=True)
#     # print(db2)
#     dbz = db2.drop_duplicates(subset=['uid'], keep=False)
#     # print(dbz)
#     print(f'对比保留了{len(dbz)}条')
#     return dbz
#
#
# def job():
#     '''
#     入库程序
#     '''
#     for i in range(10,26):
#
#         otherStyleTime = f'2022-02-{str(i)}'
#         print(f'开始入库{otherStyleTime}日数据')
#         db3 = dbz(otherStyleTime)
#
#         if len(db3) > 0:
#             df_to_mysql(db3)
#             print('入库完毕')
#         else:
#             print('无数据')

if __name__ == "__main__":
    # job()
    scheduler = BlockingScheduler()  # 实例化定时器
    scheduler.add_job(job, 'cron', hour=17, minute=51)
    scheduler.add_job(job, 'cron', hour=2, minute=30)
    scheduler.add_job(job, 'cron', hour=5, minute=30)
    scheduler.add_job(job, 'cron', hour=8, minute=30)
    scheduler.add_job(job, 'cron', hour=11, minute=30)
    scheduler.add_job(job, 'cron', hour=14, minute=30)
    scheduler.add_job(job, 'cron', hour=17, minute=30)
    scheduler.add_job(job, 'cron', hour=20, minute=30)
    scheduler.add_job(job, 'cron', hour=23, minute=30)
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        pass
    except SystemExit:
        print('exit')
        exit()