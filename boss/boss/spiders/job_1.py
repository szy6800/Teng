# -*- coding: utf-8 -*-
# 招聘详情
from abc import ABC
import re
import time
import copy
import pandas as pd
from sqlalchemy import create_engine
import scrapy
import json

def dbz():
    # now = datetime.datetime.now()
    # otherStyleTime = now.strftime("%Y-%m-%d")

    sql1 = f'''SELECT * FROM `job_type`;'''
    sql2 = f'''SELECT * FROM `job_type_copy1`;'''
    # print(sql)
    engine = create_engine('mysql+pymysql://root:123456@127.0.0.1:3306/stu?charset=utf8')
    engine2 = create_engine('mysql+pymysql://root:123456@127.0.0.1:3306/stu?charset=utf8')
    df = pd.read_sql(sql1, engine)
    df = df.drop_duplicates(subset=['id']) # 默认保留一条重复数据
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
    # print(f'对比保留了{len(dbz)}条')
    dbz = dbz[['big_type','mid_type','small_type','small_code']].values.tolist() # df转列表
    # print(dbz)
    return dbz


class Job1Spider(scrapy.Spider, ABC):
    name = 'job_1'

    def __init__(self, *args, **kwargs):
        super(Job1Spider, self).__init__()
        self.result = dbz()

    def start_requests(self):
        for i in self.result[0:1]:
            item = dict()
            item['big_type'] = i[0]
            # 小行业名称
            item['small_type'] = i[2]
            # 行业编码
            item['small_code'] = i[3]
            url = 'https://www.zhipin.com/wapi/zpgeek/search/joblist.json?scene=1&query=&city=101010100&' \
                  'experience=&degree=&industry=&scale=&stage' \
                  '=&position={}&salary=&multiBusinessDistrict=&page=1&pageSize=30'.format(item['small_code'])
            # print(url)
            yield scrapy.Request(url, callback=self.parse, dont_filter=True,
                                 meta={'item': copy.deepcopy(item)})

    def parse(self, response, *args, **kwargs):
        item = response.meta['item']
        job_text = json.loads(response.text)
        print(job_text)
        job_list = job_text['zpData']['jobList']

        for i in job_list:
            # 招聘人
            item['bossName'] = i['bossName']
            # 岗位名称
            item['jobName'] = i['jobName']
            # 薪资
            item['salaryDesc'] = i['salaryDesc']
            # 招聘人岗位
            item['bossTitle'] = i['bossTitle']
            # 岗位（标签要求）
            item['jobLabels'] = i['jobLabels']
            # 要求技能
            item['skills'] = i['skills']
            # 工作年限
            item['jobExperience'] = i['jobExperience']
            # 学历要求
            item['jobDegree'] = i['jobDegree']
            # 所在城市
            item['cityName'] = i['cityName']
            # 公司
            item['brandName'] = i['brandName']
            # 公司logo
            item['brandLogo'] = i['brandLogo']
            # 融资阶段
            item['brandStageName'] = i['brandStageName']
            # 行业
            item['brandIndustry'] = i['brandIndustry']
            # 公司规模
            item['brandScaleName'] = i['brandScaleName']
            # 公司福利
            item['welfareList'] = i['welfareList']
            # 行业编码
            item['industry'] = i['industry']
            # 城市编码
            item['cityCode'] = i['industry']

            yield item






