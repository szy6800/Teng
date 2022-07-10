#-*-coding:utf-8-*-
import time
import re
import json
import requests
import pymysql
import pandas as pd
from requests.adapters import HTTPAdapter
from lxml import etree
from 点评经纬度.tools import *
from sqlalchemy import create_engine


class AddrLng():

    def __init__(self):
        self.browser = login('')
        self.browser.implicitly_wait(10)
        # self.browser.get('https://account.dianping.com/login?redir=http%3A%2F%2Fwww.dianping.com%2F')  # 登陆页面
        # time.sleep(20)


    def start(self,d_list):
        # print(d_list)
        # self.browser.get('https://account.dianping.com/login?redir=http%3A%2F%2Fwww.dianping.com%2F')  # 登陆页面
        # time.sleep(30)
        new_url = d_list[1]
        print(d_list[0])
        self.browser.get(new_url)  # 详情页
        html = self.browser.page_source.encode("utf8").decode("utf8")  # 页面转码,防止乱码数据
        time.sleep(10)
        etrr = etree.HTML(html)  # 实例化页面
        shop_list = analysis(d_list, etrr)
        if shop_list == []:
            return []
        uid = id_map(new_url)
        frist_url = f'https://m.dianping.com/shop/{uid}/map'
        # print(frist_url)
        self.browser.get(frist_url)  # 经纬度页面

        # self.browser.find_elements_by_id('app')
        time.sleep(10)
        map_html = self.browser.page_source.encode("utf8").decode("utf8")  # 页面转码,防止乱码数据
        map_list = lng_lat(shop_list,map_html)
        # print(map_list)
        return map_list


if __name__ == '__main__':
    table1 = 'dianping2021_shangchang_pro'
    table2 = ''
    db = 'crawler2021'
    sheng = '陕西'
    count = '杨陵区'
    '''碑林区  高新区  雁塔区  莲湖区  新城区  未央区  长安区  灞桥区  临潼区  鄠邑区  高陵县  蓝田县  阎良区  周至县'''
    AddrLng = AddrLng()
    dbz = dbz('太原市')
    print(len(dbz))
    shop_list = []
    for i in dbz[400:]:
        map_ls = AddrLng.start(i)
        if map_ls == []:
            map_ls = i
            for i in range(7):
                map_ls.append('')
        shop_list.append(map_ls)
        print(shop_list)
        if len(shop_list) > 10:
            df2 = pd.DataFrame(data=shop_list)
            df2.columns = ['id', 'link', 'title', 'city', 'grade', 'capita', 'addr', 'tel', 'gr_num', 'lng', 'lat']
            df2 = df2.drop_duplicates(subset="id")

            # 保存数据
            for county in df2['city'].unique().tolist():
                dfsave = df2[df2['city'] == county]
                dfsave = compare_data(dfsave, table1, county, db=db)
                print('%s-对比后保存%d条！' % (county, len(dfsave)), end=',')
                df_to_mysql(dfsave, table1, db=db)

            shop_list = []



