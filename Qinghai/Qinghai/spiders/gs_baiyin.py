
import scrapy
import copy
from Qinghai.tools.utils import Utils_
from Qinghai.tools.DB_mysql import *
from Qinghai.tools.re_time import Times
import datetime
import jsonpath
import json
import re


class GsBaiyinSpider(scrapy.Spider):
    name = 'gs_baiyin'
    # allowed_domains = ['baiyin,gov.cn']
    def __init__(self, *args, **kwargs):
        super(GsBaiyinSpider, self).__init__()
        # self.cates = [
        #     {"cate": "000", "pages": 2},  # 招标公告
        #     # {"cate": "001", "pages": 1},  # 变更公告
        #     # {"cate": "002", "pages": 1},  # 候选人公示
        #     # {"cate": "003", "pages": 1},  # 中标\流标公告
        # ]
        self.t = Times()
        self.c_time = datetime.datetime.utcnow() - datetime.timedelta(days=7)

    def start_requests(self):
        for i in range(1, 2):
            url = "http://ggzyjy.baiyin.gov.cn/ajax/InfoPage_TradeInfomation,App_Web_tradeinfomation.aspx.3db62" \
                  "916.nnssip8r.ashx?_method=getTradeDataList&_session=no"
            data = '''infoType=0
                        curr=1
                        keywords=
                        queryStr=and  a.PrjPropertyNew in (1,2,3,21,22,23,24,5,6,12,13,14,15,16,17,18,19,20,4,7,8,9,11,41,31,44,43,45,711,441,442,443,0,331,332,333,0) and a.Field1 in(3259,2955,2956,2957,2958,2959,2960)'''
            yield scrapy.Request(url=url, body=json.dumps(data), callback=self.parse,method='POST')

    def parse(self, response, **kwargs):
        print(response.text)