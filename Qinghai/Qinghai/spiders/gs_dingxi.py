# -*- coding: utf-8 -*-

# @Author : 石张毅
# @Site : http://ggzy.dingxi.gov.cn/jyxx/project.html?categoryNum=
# @introduce: 甘肃省紫色字幕 定西市公共资源交易中心
# @time: 2022/5/07

import scrapy
import scrapy
import copy
from Qinghai.tools.utils import Utils_
from Qinghai.tools.DB_mysql import *
from Qinghai.tools.re_time import Times
import datetime
import jsonpath
import json
import re


class GsDingxiSpider(scrapy.Spider):
    name = 'gs_dingxi'

    def __init__(self, *args, **kwargs):
        super(GsDingxiSpider, self).__init__()
        # self.cates = [
        #
        #     {"cate": "000", "pages": 2},  # 招标公告
        #     # {"cate": "001", "pages": 1},  # 变更公告
        #     # {"cate": "002", "pages": 1},  # 候选人公示
        #     # {"cate": "003", "pages": 1},  # 中标\流标公告
        #
        # ]
        self.t = Times()
        self.c_time = datetime.datetime.utcnow() - datetime.timedelta(days=7)

    def start_requests(self):
        for i in range(1, 9):
            url = "http://ggzy.dingxi.gov.cn/EpointWebBuilder/JySearchAction.action?cmd=initPageList"
            formdata = {
                "siteGuid": "7eb5f7f1-9041-43ad-8e13-8fcb82ea831a",
                "categorynum": "004",
                "citycode": "",
                "jylb": "",
                "jylx": "",
                "title": "",
                "pageIndex": "{}".format(i),
                "pageSize": "20",
                "verificationGuid": "",
                "verificationCode": "",
            }
            yield scrapy.FormRequest(url=url, formdata=formdata, callback=self.parse)

    def parse(self, response, **kwargs):
        json_text = json.loads(response.text)

        # print(json_text)

        infoid = re.findall('"infoid":"(.*?)",', str(json_text))
        types = re.findall('"lbname":"(.*?)",', str(json_text))
        for infoid,types in zip(infoid,types):
            if types =='工程建设':
                tid = 'A01'
            elif types == '政府采购':
                tid = 'M01'
            else:
                continue
            item = dict()
            item['link'] = 'http://ggzy.dingxi.gov.cn/EpointWebServiceDx/rest/DXProjectInfotoweb/ge' \
                           'tProjectinfo?infoid={}&infotype={}'.format(infoid, tid)

            # print(item['link'])
            yield scrapy.Request(item['link'], callback=self.parse_info, meta={'item': copy.deepcopy(item), 'types':types},
                                 dont_filter=True)

    def parse_info(self,response):
        json_text = json.loads(response.text)
        if response.status != 200:
            return
        item = response.meta['item']
        types = response.meta['types']
        item['title'] = jsonpath.jsonpath(json_text,'$..projectname')[0]
        pub_time = jsonpath.jsonpath(json_text,'$..sbrdate')[0]
        PUBLISH = self.t.datetimes(pub_time)
        item['publish_time'] = PUBLISH.strftime('%Y-%m-%d')  # 发布时间
        # print(item['link'], item['publish_time'], item['title'])
        ctime = self.t.datetimes(item['publish_time'])
        if ctime < self.c_time:
            print('文章发布时间大于规定时间，不予采集', item['link'])
            return
        # 标题
        item['uuid'] = ''
        item['uid'] = 'zf' + Utils_.md5_encrypt(item['title'] + item['link'] + item['publish_time'])
        item['intro'] = ''
        item['abs'] = '1'
        item['content'] =jsonpath.jsonpath(json_text,'$..zhaobiaofanwei')[0]
        item['purchaser'] = jsonpath.jsonpath(json_text,'$..jianshedanwei')[0]
        item['create_time'] = str(datetime.datetime.now().strftime('%Y-%m-%d'))
        item['proxy'] = ''
        item['update_time'] = ''
        from Qinghai.tools.uredis import Redis_DB
        if Redis_DB().Redis_pd(item['uid']) is True:  #数据去重
            print(item['uid'], '\033[0;35m <=======此数据已采集=======> \033[0m')
            return
        item['deleted'] = ''
        item['province'] = '甘肃省'
        item['base'] = ''
        item['type'] = types
        item['items'] = ''
        item['data_source'] = '00396'
        item['end_time'] = ''
        item['status'] = ''
        item['serial'] = jsonpath.jsonpath(json_text,'$..projectno')[0]

        yield item




