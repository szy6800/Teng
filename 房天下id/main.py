#-*-coding:utf-8-*-
import time
import re
import json
import requests
import pymysql
import pandas as pd
from requests.adapters import HTTPAdapter
from lxml import etree
from 房天下id.tools import *
from sqlalchemy import create_engine


class AddrLng():

    def __init__(self):
        self.browser = login('')
        self.browser.implicitly_wait(10)
        self.L = {'海东': 'https://haidong.esf.fang.com/housing/'}
        # self.F = {'兴宁': 'https://nn.esf.fang.com/housing/431', '江南': 'https://nn.esf.fang.com/housing/434', '邕宁': 'https://nn.esf.fang.com/housing/436', '青秀': 'https://nn.esf.fang.com/housing/1131', '西乡塘': 'https://nn.esf.fang.com/housing/1132', '良庆': 'https://nn.esf.fang.com/housing/1133', '北海': 'https://nn.esf.fang.com/housing/16805', '钦州': 'https://nn.esf.fang.com/housing/16806', '防城港': 'https://nn.esf.fang.com/housing/11539', '武鸣': 'https://nn.esf.fang.com/housing/14677', '宾阳': 'https://nn.esf.fang.com/housing/16705', '横县': 'https://nn.esf.fang.com/housing/16706', '其他': 'https://nn.esf.fang.com/housing/16578'}
        self.table1 = 'ershouid'
        self.table2 = ''
        self.db = 'test'
        self.sheng = '陕西'

    def start(self):
        for k,v in self.L.items():
            new_url = v + f'__0_3_0_0_1_0_0_0/'
            self.browser.get(new_url)
            time.sleep(5)
            self.browser.get(new_url)
            time.sleep(4)
            html = self.browser.page_source.encode("utf8").decode("utf8")  # 页面转码,防止乱码数据
            etrr = etree.HTML(html)  # 实例化页面
            shop_list = analysis(etrr,k)
            df2 = pd.DataFrame(data=shop_list)
            df2.columns = ['uid', 'id', 'county']
            df2 = df2.drop_duplicates(subset="id")
            # df2[['link', 'id']].values.tolist()

            for county in df2['county'].unique().tolist():
                dfsave = df2[df2['county'] == county]
                dfsave = compare_data(dfsave, self.table1, county, db=self.db)
                print('%s-对比后保存%d条！' % (county, len(dfsave)), end=',')
                df_to_mysql(dfsave, self.table1, db=self.db)

            try:
                conut_numer = etrr.xpath('//span[@class="txt"]/text()')[0]  # 一共的页数
                conut_numer = conut_numer[1:-1]
                print(f'一共{conut_numer}页数据')
                if int(conut_numer) >= 2:
                    for i in range(2, int(conut_numer) + 1):
                        first_url = new_url = v + f'__0_3_0_0_{str(i)}_0_0_0/'
                        self.browser.get(first_url)  # 列表页
                        time.sleep(5)
                        htmls = self.browser.page_source.encode("utf8").decode("utf8")  # 页面转码,防止乱码数据
                        etrr = etree.HTML(htmls)  # 实例化页面
                        shop_list = analysis(etrr, k)
                        df2 = pd.DataFrame(data=shop_list)
                        df2.columns = ['uid', 'id', 'county']
                        df2 = df2.drop_duplicates(subset="id")
                        # df2[['link', 'id']].values.tolist()

                        for county in df2['county'].unique().tolist():
                            dfsave = df2[df2['county'] == county]
                            dfsave = compare_data(dfsave, self.table1, county, db=self.db)
                            print('%s-对比后保存%d条！' % (county, len(dfsave)), end=',')
                            df_to_mysql(dfsave, self.table1, db=self.db)

            except:
                print('共一页')
            # self.browser.get(v + '__0_3_0_0_2_0_0_0/')
            # time.sleep(4)
            # html = self.browser.page_source.encode("utf8").decode("utf8")  # 页面转码,防止乱码数据
            # print(html)



if __name__ == '__main__':
    AddrLng = AddrLng()
    AddrLng.start()

