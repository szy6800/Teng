# -*- coding: utf-8 -*-

# @Author : 石张毅
# @Site :
# @introduce:

import scrapy
import copy
from Qinghai.tools.utils import Utils_
from Qinghai.tools.DB_mysql import *
from Qinghai.tools.re_time import Times
import datetime
import jsonpath
import json


class GsGgzyjySpider(scrapy.Spider):
    name = 'gs_ggzyjy'

    def __init__(self, *args, **kwargs ):
        super(GsGgzyjySpider, self).__init__()
        # self.cates = [
        #
        #     {"cate": "000", "pages": 2},  # 招标公告
        #     # {"cate": "001", "pages": 1},  # 变更公告
        #     # {"cate": "002", "pages": 1},  # 候选人公示
        #     # {"cate": "003", "pages": 1},  # 中标\流标公告
        #
        # ]
        self.t = Times()
        self.c_time = datetime.datetime.utcnow() - datetime.timedelta(days=2)

    def start_requests(self):
        url = "http://ggzyjy.baiyin.gov.cn/ajax/InfoPage_TradeInfomation,App_Web_tradeinfomation.aspx.3db62916.arderj2p.ashx?_method=getTradeDataList&_session=no"

        formdata = 'infoType=0curr=3keywords=queryStr=and  a.PrjPropertyNew in (1,2,3,21,22,23,24,5,6,12,13,14,15,16,17,18,19,20,4,7,8,9,11,41,31,44,43,45,711,441,442,443,0,331,332,333,0) and a.Field1 in(3259,2955,2956,2957,2958,2959,2960)'
        yield scrapy.FormRequest(url=url, body=formdata, callback=self.parse)

    def parse(self, response, **kwargs):
        print(response.text)

