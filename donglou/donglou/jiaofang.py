import datetime
import json

import scrapy
import re
import time

from copy import deepcopy
import numpy as np
import pandas as pd
from sqlalchemy import create_engine
# from loupan_f.items import ArchendItem
from loupan_f.items import Decorate

def queryue(sql):
    engine = create_engine('mysql+pymysql://root:Lxp.138927!asd@123.126.87.123:3306/crawler2021?charset=utf8')

    df = pd.read_sql_query(sql, engine)

    lists1 = np.array(df)

    lists = lists1.tolist()
    # print(lists)
    return lists

# 模糊查询
"""SELECT * FROM meituan2 WHERE url LIKE '%fz.meituan.com%';"""

def id_sult():
    # sql = """SELECT * FROM ershou WHERE dongnum = '暂无资料栋';"""
    sql = """SELECT uid,arch_id FROM arch_info_crawler WHERE source_name='房天下新房';"""
    result1 = queryue(sql=sql)
    page = len(result1)
    print(f'========读取总数>>{page}条=======')
    # print(result1)
    result = []
    for i in range(page):
        result.append(result1[i])
    print('=========读取完毕=========')
    return result


class JiaofangSpider(scrapy.Spider):
    name = 'jiaofang'
    # allowed_domains = ['www.c']
    # start_urls = ['http://www.c/']

    def __init__(self, *args, **kwargs):
        super(JiaofangSpider, self).__init__()
        self.L = {
            'zbgg': '招标公告',
        }
        self.result = id_sult()

    def start_requests(self):
        for ids in self.result:
            # print(new_url)
            uid = ids[0]
            # time.sleep(1.6)
            new_url = f'https://xian.newhouse.fang.com/loupan/{ids[1]}/housedetail.htm'
            yield scrapy.Request(new_url, callback=self.parse, meta={'uid': uid})

    def parse(self, response):
        # print(response.text)
        uid = response.meta['uid']
        item = Decorate()
        item['uid'] = uid
        # item['archend_time'] = response.xpath("//*[contains(text(),'交房时间')]/following-sibling::div[1]/text()").get()
        item['Decorate_state'] = response.xpath("//*[contains(text(),'装修状况')]/following-sibling::div[1]/a/text()").get()
        print(item)
        yield item