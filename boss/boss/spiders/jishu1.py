# -*- coding: utf-8 -*-

# @Author : 石张毅
# @Site :
# @introduce:

import scrapy
import re
import time
import requests
import copy
from copy import deepcopy
from sqlalchemy import create_engine
# from loupan.items import LoupanItem
import numpy as np
import pandas as pd
import scrapy


def list_str(con):
    sss = ''
    for i in con:
        sss = sss + i
    return sss.strip()

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

dbz()
class Jishu1Spider(scrapy.Spider):
    name = 'jishu1'
    # allowed_domains = ['boss.com']
    # start_urls = ['http://boss.com/']

    def __init__(self, *args, **kwargs):
        super(Jishu1Spider, self).__init__()
        self.result = dbz()

    def start_requests(self):
        for i in self.result[0:1]:
            item = dict()
            item['big_type'] = i[0]
            item['small_type'] = i[2]
            item['small_code'] = i[3]
            url = 'https://www.zhipin.com/c100010000-p{}/?page=2'.format(item['small_code'])
            yield scrapy.Request(url, callback=self.parse,dont_filter=True,meta={'item':deepcopy(item)})


    def parse(self, response, **kwargs):

        job_urls = response.xpath('//*[@class="primary-box"]/@href').getall()
        job_titles = response.xpath('//*[@class="job-name"]/a/@title').getall()
        job_area = response.xpath('//*[@class="job-area"]/text()').getall()
        salary = response.xpath('//*[@class="red"]/text()').getall()
        job_welfare = response.xpath('//*[@class="info-desc"]/text()').getall()
        company_url = response.xpath('//*[@class="company-text"]/h3/a/@href').getall()
        job_tag = response.xpath('string(//*[@class="tags"])').getall()
        for job_urls,job_titles,job_area,salary,job_welfare,company_url in zip(job_urls,job_titles,job_area,salary,job_welfare,company_url):
            # 详情链接
            item = response.meta['item']
            item['job_urls'] = response.urljoin(job_urls)
            # 工作名称
            item['job_titles'] = job_titles
            # 工作地区
            item['job_area'] = job_area
            # 薪资
            item['salary'] = salary
            # 工作福利
            item['job_welfare'] = job_welfare
            # 公司链接
            item['company_url'] = response.urljoin(company_url)
            yield scrapy.Request(item['job_urls'], callback=self.parse_info, dont_filter=True, meta={'item': deepcopy(item)})


    def parse_info(self,response):
        item = response.meta['item']
        # 城市
        item['city'] = response.xpath('//*[@class="text-city"]/text()').get()
        # 工作年限
        item['work_time'] = response.xpath('//*[@class="text-city"]/following::text()[1]').get()
        # 学历
        item['education'] = response.xpath('//*[@class="text-city"]/following::text()[2]').get()
        # hr
        item['hr'] = response.xpath('//h2[@class="name"]/text()[1]').get()
        # hr岗位
        hr_position = response.xpath('//h2[@class="name"]/following::p[1]//text()').getall()
        item['hr_position'] = list_str(hr_position)
        # 岗位详情
        j_content = response.xpath('//h3/following::div[@class="text"]//text()').getall()
        item['job_dec'] = list_str(j_content)

        yield item







