import datetime
import hashlib
from sqlalchemy import create_engine
import numpy as np
import pandas as pd


def queryue(sql):
    # 数据库连接
    # engine = create_engine('mysql+pymysql://root:I0z>kp9tnavw@123.56.87.41:3306/crawler2021?charset=utf8')
    engine = create_engine('mysql+mysqlconnector://root:123456@127.0.0.1:3306/ceshi?charset=utf8')
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
    # 数据库操作
    # now = datetime.datetime.utcno
    #
    #
    # w() - datetime.timedelta(days=1)
    now = datetime.datetime.utcnow()
    otherStyleTime = now.strftime("%Y-%m-%d")
    sql = f"SELECT uid,uuid,title,link,intro,abs,content,publish_time,purchaser,proxy,create_time,update_time,deleted,province,base,type,items,data_source,end_time,status,serial FROM `caijiqi` WHERE abs='3' AND create_time>'{otherStyleTime}';"
    result1 = queryue(sql=sql)
    result = []
    nows = datetime.datetime.now()
    otherStyleTimes = nows.strftime("%Y-%m-%d")
    for i in range(len(result1)):
        result1[i][0] = md5_encrypt(result1[i][2]+result1[i][3]+result1[i][7])
        result1[i][10] = otherStyleTimes
        result.append(result1[i])
    return result


def df_to_mysql(df):
    # 入库
    df.to_sql(name = 'zhaobiao2021',
            con = 'mysql+pymysql://root:123456@127.0.0.1:3306/ceshi?charset=utf8',
            # con = 'mysql+pymysql://root:I0z>kp9tnavw@123.56.87.41:3306/crawler2021?charset=utf8',
            if_exists = 'append',index=False,
    chunksize=20000)


def dbz():
    # 批量去重，返回去重后数据
    now = datetime.datetime.now()
    otherStyleTime = now.strftime("%Y                                       -%m-%d")
    sql = f'''SELECT uid,uuid,title,link,intro,abs,content,publish_time,purchaser,proxy,create_time,update_time,deleted,province,base,type,items,data_source,end_time,status,serial FROM `zhaobiao2021` WHERE create_time='{otherStyleTime}' AND abs='3';'''
    # sql = '''SELECT uid,uuid,title,link,intro,abs,content,publish_time,purchaser,proxy,create_time,update_time,deleted,province,base,type,items,data_source,end_time,status,serial FROM `zhaobiao2021` WHERE create_time='2021-10-19';'''
    # print(sql)
    # engine = create_engine('mysql+pymysql://root:@127.0.0.1:3306/test?charset=utf8')
    engine2 = create_engine('mysql+pymysql://root:123456@127.0.0.1:3306/ceshi?charset=utf8')
    # df = pd.read_sql(sql, engine)
    # print(df)
    df1 = pd.read_sql(sql, engine2) # 获取数据库数据
    results = id_sult()

    df2 = pd.DataFrame(data=results)
    df2.columns = ['uid', 'uuid', 'title', 'link', 'intro', 'abs', 'content', 'publish_time',
                   'purchaser', 'proxy', 'create_time', 'update_time', 'deleted', 'province', 'base',
                   'type', 'items', 'data_source', 'end_time', 'status', 'serial']# 列表转化为PD格式
    df2 = df2.drop_duplicates(subset="uid") # uid去重
    # engine.dispose()
    engine2.dispose() # 关闭连接
    # print(df1)
    db2 = pd.concat([df2, df1], axis=0, sort=False, ignore_index=True) # 合并数据
    # print(db2)
    dbz = db2.drop_duplicates(subset=['uid'], keep=False) # 根据uid去重，keep=False不保留重复数据
    # print(dbz)
    print(f'对比保留了{len(dbz)}条')
    return dbz


db3 = dbz()
df_to_mysql(db3)

