from sqlalchemy import create_engine
import pymysql
from sqlalchemy.types import *
import numpy as np
import pandas as pd
import time
import json
from 点评商场.tools import *

import re
import requests
def queryue(sql):
    # engine = create_engine('mysql+pymysql://root:I0z>kp9tnavw@127.0.0.1:3306/crawler2021?charset=utf8')
    engine = create_engine('mysql+pymysql://root:123456@127.0.0.1:3306/test?charset=utf8')
    df = pd.read_sql_query(sql, engine)
    lists1 = np.array(df)
    lists = lists1.tolist()
    # print(lists)
    return lists


# 模糊查询
"""SELECT * FROM meituan2 WHERE url LIKE '%fz.meituan.com%';"""

def dbz():
    # now = datetime.datetime.now()
    # otherStyleTime = now.strftime("%Y-%m-%d")
    sql1 = f'''SELECT id,url,link,title,county FROM `dianping2021`;'''
    sql2 = f'''SELECT fid FROM `dianping2021_dianpuid` ;'''
    # print(sql)
    engine = create_engine('mysql+pymysql://root:Lxp.138927!asd@123.126.87.123:3306/crawler2021?charset=utf8')
    engine2 = create_engine('mysql+pymysql://root:123456@127.0.0.1:3306/test?charset=utf8')
    df = pd.read_sql(sql1, engine)
    df = df.drop_duplicates(subset=['id']) # 默认保留一条重复数据
    # print(df)
    df1 = pd.read_sql(sql2, engine2)
    df1 = df1.drop_duplicates(subset=['fid'])  # 默认保留一条重复数据
    engine.dispose()
    engine2.dispose()
    # print(df1)
    db2 = pd.concat([df, df1], axis=0, sort=False, ignore_index=True)
    # print(db2)
    dbz = db2.drop_duplicates(subset=['fid'], keep=False)
    # print(dbz)
    print(f'对比保留了{len(dbz)}条')
    dbz = dbz[['fid','title']].values.tolist() # df转列表
    print(dbz)
    return dbz

dbz()
# dbz('闽侯县')

# def id_sult():
#     # sql = 'SELECT * FROM meituan1 WHERE 地市详情链接="http://nd.meituan.com/meishi"'
#     # sql = 'SELECT * FROM zhaobiao2021;'
#     sql = f"SELECT * FROM `dianping2021_shangchang` WHERE province='山西省' AND jsons!='无';"
#     result1 = queryue(sql=sql)
#     page = len(result1)
#     print(f'========读取总数>>{page}条=======')
#     # print(result1)
#     # print(result1)
#     result = []
#     for i in range(page):
#         result.append(result1[i])
#     print('=========读取完毕=========')
#     return result
#
# def df_to_mysql(df_all, table2, db):
#     df_save = df_all
#     if len(df_save) >= 0:
#         try:
#             engine = create_engine('mysql+pymysql://root:123456@127.0.0.1:3306/{}?charset=utf8'.format(db))
#             df_save.to_sql(name=table2,
#                            con=engine,
#                            if_exists='append', index=False,
#                            chunksize=10000)
#             print('保存了%d条数据！' % len(df_save))
#             engine.dispose()
#         except Exception as e:
#             df_save.to_csv('./tomysql_error2.csv', index=False)
#             print(e)
#             input01 = input('写入数据库错误')
#
#             # 抓取之前对比数据库
#
#
# class AddrLng():
#
#     def __init__(self):
#         # self.browser = login('')
#         # self.browser.implicitly_wait(10)
#         # result = id_sult()
#         # df2 = pd.DataFrame(data=result)
#         # df2.columns = ['province', 'city', 'county', 'district', 'analysis', 'title', 'url', 'link', 'id']
#         # self.df2 = df2.drop_duplicates(subset="id")
#         self.df2 = id_sult()
#
#
#     def start(self):
#         # print(d_list)
#         shangchenglist = []
#         for d_list in self.df2[13:]:
#             print(d_list)
#             shoping_list = []
#             city = d_list[1]
#             uid = d_list[8]
#             count_list = json.loads(d_list[9])
#             shopid = re.search('//pages/list/list\?mallId=(.*)', count_list[0]['listUrl']).group(1)
#             for count in count_list[1:]:
#                 cateId = count['cateId']
#                 for t in count['tagList']:
#                     tag = t['name']
#                     typ = t['type']
#                     time.sleep(10)
#                     url = f'https://mapi.dianping.com/shopping/navipoilist?version=9.0.0&shopid={shopid}&shopIdL={shopid}&cityid=2&cateid={cateId}&tag={tag}&type={typ}'
#
#                     headers = {
#                         "Accept": "*/*",
#                         "Accept-Encoding": "gzip, deflate, br",
#                         "Accept-Language": "zh-CN,zh;q=0.9",
#                         "Connection": "keep-alive",
#                         "Cookie": '_lxsdk_cuid=17d311b3888b7-00a24984c52fa1-b7a1438-384000-17d311b3889c8; _lxsdk=17d311b3888b7-00a24984c52fa1-b7a1438-384000-17d311b3889c8; _hc.v=a1860f43-9deb-625f-ebf5-57290c959b18.1637206408; s_ViewType=10; ctu=d556d8e73a270d3894747b895579b86389799a37d028708b158e4b3c033dd1dc; _dp.ac.v=add6f9a8-2a3c-43c1-b312-9faf4698c54d; aburl=1; Hm_lvt_dbeeb675516927da776beeb1d9802bd4=1649759442,1649818197; Hm_lvt_4c4fc10949f0d691f3a2cc4ca5065397=1650267509; fspop=test; Hm_lvt_602b80cf8079ae6591966cc70a3940e7=1654152108,1654492349,1656297622; _lx_utm=utm_source%3DBaidu%26utm_medium%3Dorganic; cityid=2; default_ab=map%3AA%3A1; m_flash2=1; cy=35; cye=taiyuan; WEBDFPID=6v80429u4w285w16z6v242351858vzxv818y17w42u697958yu143x2x-1656738788161-; Hm_lpvt_602b80cf8079ae6591966cc70a3940e7=1656654696; pvhistory="6L+U5ZuePjo8L3Nob3AvRzNMY0pORjFvaXBKTDgwSCZzaG9wdHlwZT0xMCZjaXR5aWQ9NDQ4NyZzaG9wY2F0ZWdvcnlpZD0zNDIzNz46PDE2NTY2NjcxMTU1NjBdX1s="; _lxsdk_s=181b8d18840-92a-3a6-f74%7C0%7C155',
#                         "Host": "mapi.dianping.com",
#                         "Origin": "https://m.dianping.com",
#                         "Referer": "https://m.dianping.com/",
#                         "sec-ch-ua": "\" Not A;Brand\";v=\"99\", \"Chromium\";v=\"96\", \"Google Chrome\";v=\"96\"",
#                         "sec-ch-ua-mobile": "?1",
#                         "sec-ch-ua-platform": "\"Android\"",
#                         "Sec-Fetch-Dest": "empty",
#                         "Sec-Fetch-Mode": "cors",
#                         "Sec-Fetch-Site": "same-site",
#                         "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Mobile Safari/537.36"
#                     }
#
#                     response = requests.get(url, headers=headers)
#                     print(response.text)
#                     respon = json.loads(response.text)
#                     cout_list = respon['msg']['list']
#                     for cout in cout_list:
#                         item = []
#                         item.append(city)
#                         item.append(uid)
#                         try:
#                             url = re.search('(.*?)&shoptype=',cout['jumpUrl']).group(1)
#                         except:
#                             url = cout['jumpUrl']
#                         item.append(cout['title'])
#                         item.append(url)
#                         item.append(cout['shopuuid'])
#                         print(item)
#                         shoping_list.append(item)
#             print('保存了')
#             if shoping_list == []:
#                 continue
#             df1 = pd.DataFrame(data=shoping_list)
#             df1.columns = ['city', 'fid', 'title', 'link', 'id']
#             df_to_mysql(df1, 'dianping2021_dianpuid', 'test')
#
#
#
#
#
#
#                 # break
#             # break
#
#
#
#             # new_url = d_list[7]
#             # # new_url = 'https://m.dianping.com/shop/l2xBxMtsWIf7CezP?source=pc_jump'
#             # self.browser.get(new_url)  # 详情页
#             # html = self.browser.page_source.encode("utf8").decode("utf8")  # 页面转码,防止乱码数据
#             # time.sleep(10)
#             # # etrr = etree.HTML(html)  # 实例化页面
#             # shop_list = analysis(d_list, html)
#             # # print(shop_list)
#             # shangchenglist.append(shop_list)
#             # # break
#             # print(shangchenglist)
#             # if len(shangchenglist) == 50:
#             #     df1 = pd.DataFrame(data=shangchenglist)
#             #     df1.columns = ['province', 'city', 'county', 'district', 'analysis', 'title', 'url', 'link', 'id','jsons']
#             #     df_to_mysql(df1, 'dianping2021_shangchang', 'test')
#             #     shangchenglist = []
#
#
#
# if __name__ == '__main__':
#     AddrLng = AddrLng()
#     AddrLng.start()