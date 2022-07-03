from sqlalchemy import create_engine
import pymysql
from sqlalchemy.types import *
import numpy as np
import pandas as pd
from PROJECT.新建文件夹.点评商场.tools import *

def queryue(sql):
    # engine = create_engine('mysql+pymysql://root:I0z>kp9tnavw@127.0.0.1:3306/crawler2021?charset=utf8')
    engine = create_engine('mysql+pymysql://root:q!dwyyl6:q3L@127.0.0.1:3306/test?charset=utf8')

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
    sql = f"SELECT * FROM `dianping2021` WHERE province='山西省' AND analysis='商场';"
    result1 = queryue(sql=sql)
    page = len(result1)
    print(f'========读取总数>>{page}条=======')
    # print(result1)
    # print(result1)
    result = []
    for i in range(page):
        result.append(result1[i])
    print('=========读取完毕=========')
    return result



class AddrLng():

    def __init__(self):
        self.browser = login('')
        self.browser.implicitly_wait(10)
        result = id_sult()
        df2 = pd.DataFrame(data=result)
        df2.columns = ['province', 'city', 'county', 'district', 'analysis', 'title', 'url', 'link', 'id']
        self.df2 = df2.drop_duplicates(subset="id")


    def start(self):
        # print(d_list)
        shangchenglist = []
        for i in self.df2.values:
            d_list = []
            for x in i:
                d_list.append(x)
            print(d_list)
            new_url = d_list[7]
            # new_url = 'https://m.dianping.com/shop/l2xBxMtsWIf7CezP?source=pc_jump'
            self.browser.get(new_url)  # 详情页
            html = self.browser.page_source.encode("utf8").decode("utf8")  # 页面转码,防止乱码数据
            time.sleep(10)
            # etrr = etree.HTML(html)  # 实例化页面
            shop_list = analysis(d_list, html)
            # print(shop_list)
            shangchenglist.append(shop_list)
            # break
            print(shangchenglist)
            if len(shangchenglist) == 50:
                df1 = pd.DataFrame(data=shangchenglist)
                df1.columns = ['province', 'city', 'county', 'district', 'analysis', 'title', 'url', 'link', 'id','jsons']
                df_to_mysql(df1, 'dianping2021_shangchang', 'test')
                shangchenglist = []



if __name__ == '__main__':
    AddrLng = AddrLng()
    AddrLng.start()