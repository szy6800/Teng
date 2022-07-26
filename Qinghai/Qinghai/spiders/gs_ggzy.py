# -*- coding: utf-8 -*-

# @Time : 2022-07-26 15:14:30
# @Author : 石张毅
# @Site : http://deal.ggzy.gov.cn/ds/deal/dealList.jsp
# @introduce: 全国公共资源交易平台

import copy
from Qinghai.tools.utils import Utils_
from Qinghai.tools.DB_mysql import *
from Qinghai.tools.re_time import Times
from lxml import etree
import datetime
import jsonpath
import json
from Qinghai.tools.uredis import Redis_DB
import scrapy


class GsGgzySpider(scrapy.Spider):
    name = 'gs_ggzy'
    allowed_domains = ['baicu.com']

    def __init__(self, *args, **kwargs):
        super(GsGgzySpider, self).__init__()
        self.cates = [
            # {"cate": "ZBGG", "pages": 2,'types':'SZFJ'},  # 市政、房建工程
            # {"cate": "CGGG", "pages": 2,'types':'ZFCG'},  # 政府采购
            # {"cate": "ZBGG", "pages": 2,'types':'QT'},  # 交通、水利及其他工程
            # {"cate": "CRGG", "pages": 2,'types':'GTGC'},  # 国土、矿权、产权
            # {"cate": "ZBGG", "pages": 2,'types':'GYXM'},  # 工业项目
        ]
        self.t = Times()
        self.c_time = datetime.datetime.utcnow() - datetime.timedelta(days=2)

    def start_requests(self):
        for i in range(1, 7):
            url = "http://deal.ggzy.gov.cn/ds/deal/dealList_find.jsp"
            formdata = {
                "TIMEBEGIN_SHOW": "2022-07-17",
                "TIMEEND_SHOW": "2022-07-26",
                "TIMEBEGIN": "2022-07-17",
                "TIMEEND": "2022-07-26",
                "SOURCE_TYPE": "1",
                "DEAL_TIME": "02",
                "DEAL_CLASSIFY": "00",
                "DEAL_STAGE": "0000",
                "DEAL_PROVINCE": "620000",
                "DEAL_CITY": "0",
                "DEAL_PLATFORM": "0",
                "BID_PLATFORM": "0",
                "DEAL_TRADE": "0",
                "isShowAll": "1",
                "PAGENUMBER": "{}".format(i),
                "FINDTXT": "",
            }
            yield scrapy.FormRequest(url=url, formdata=formdata, callback=self.parse)
    #
    def parse(self, response, **kwargs):
        json_text = json.loads(response.text)
        count_list = json_text['data']
        for count in count_list:
            item = dict()
            link = count['url']

            item['link'] = link.replace('html/a','html/b')
            # 行业
            item['items'] = count['tradeShow']
            item['type'] = count['stageShow']
            item['title'] = count['title']
            if item['title'] is None:
                continue
            pub_time = count['timeShow']
            PUBLISH = self.t.datetimes(pub_time)
            item['publish_time'] = PUBLISH.strftime('%Y-%m-%d')  # 发
            item['uid'] = 'zf' + Utils_.md5_encrypt(item['title'] + item['link'] + item['publish_time'])
            # print(item['link'],item['title'],item['publish_time'])
            ctime = self.t.datetimes(item['publish_time'])
            if ctime < self.c_time:
                print('文章发布时间大于规定时间，不予采集', item['link'])
                return
            if Redis_DB().Redis_pd(item['uid']) is True:  # 数据去重
                print(item['uid'], '\033[0;35m <=======此数据已采集=======> \033[0m')
                continue
            yield scrapy.Request(item['link'], callback=self.parse_info, meta={'item': copy.deepcopy(item)},
                                 dont_filter=True)

    def parse_info(self, response):
        if response.status != 200:
            return
        item = response.meta['item']
        # 标题
        item['uuid'] = ''
        item['intro'] = ''
        item['abs'] = '1'
        from lxml import etree
        html = etree.HTML(response.text)
        div_data = html.xpath('//*[@id="mycontent"]')
        item['content'] = etree.tostring(div_data[0], encoding='utf-8').decode()
        item['purchaser'] = ''
        item['create_time'] = str(datetime.datetime.now().strftime('%Y-%m-%d'))
        item['proxy'] = ''
        item['update_time'] = ''
        item['deleted'] = ''
        item['province'] = '甘肃省'
        item['base'] = ''
        item['data_source'] = '00689'
        item['end_time'] = ''
        item['status'] = ''
        item['serial'] = ''
        # print(item)

        yield item
