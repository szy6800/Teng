# -*- coding: utf-8 -*-

# @Author : 石张毅
# @Site : 阿拉善公共资源交易网  http://alsggzyjy.cn/


import scrapy
import copy
from Qinghai.tools.utils import Utils_
from Qinghai.tools.DB_mysql import *
from Qinghai.tools.re_time import Times
import datetime
import jsonpath
import json


class AlsggzyjySpider(scrapy.Spider):
    name = 'alsggzyjy'
    # allowed_domains = ['alsggzyjy.cn']
    # start_urls = ['http://alsggzyjy.cn/']

    def __init__(self, *args, **kwargs ):
        super(AlsggzyjySpider, self).__init__()
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
        url = "http://www.dgsy.com.cn//www/main.jsp?f_treeCode=00190001"

        formdata = {
            'pagenumber': '6',

        }
        yield scrapy.FormRequest(url=url, formdata=formdata, callback=self.parse)

    # def start_requests(self):
    #     for each in self.cates:
    #         cate = each["cate"]
    #         pages = each["pages"]
    #         for p in range(pages):
    #             p = f"{p}" if p else ""
    #             url = f"http://www.alsggzyjy.cn/PublicServer/commonAnnouncementAction/getCommonAnnouncementList.do?businessType=2&announcementType={cate}&page={p}&rows=15&areaCode=152900"
    #             yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        json_text = json.loads(response.text)
        item = {}
        # 列表页链接和发布时间
        list_id = jsonpath.jsonpath(json_text, '$..id')
        pub_times = jsonpath.jsonpath(json_text, '$..publishTime')
        # title = jsonpath.jsonpath(json_text, '$..title')
        # print(list_id,pub_times,title)
        # 循环遍历
        for href, pub_time in zip(list_id, pub_times):
            # print(response.urljoin(href))
            item['link'] = 'http://www.alsggzyjy.cn/PublicServer/public/commonAnnouncement/showDetail.html?businessType=2&sidebarIndex=4&id='+href
            PUBLISH = self.t.datetimes(pub_time)
            item['publish_time'] = PUBLISH.strftime('%Y-%m-%d')  # 发布时间
            # ctime = self.t.datetimes(item['publish_time'])
            #
            # if ctime < self.c_time:
            #     print('文章发布时间大于规定时间，不予采集', item['link'])
            #     return
            parse_url = "http://www.alsggzyjy.cn/PublicServer/commonAnnouncementAction/selectPublishAnnouncementById.do"
            formdata = {
                'id': href

            }
            # print(item['link'], item['publish_time'])
            yield scrapy.FormRequest(parse_url, formdata=formdata,callback=self.parse_info, meta={'item': copy.deepcopy(item)},)

    def parse_info(self, response):
        print(response.text)
        # detail_json = json.loads(response.text)
        # if response.status != 200:
        #     return
        # item = response.meta['item']
        # item['title'] = jsonpath.jsonpath(detail_json, '$..title')
        # print(item['title'])

        # 标题
        # item['uuid'] = ''
        # item['uid'] = 'zf' + Utils_.md5_encrypt(item['title'] + item['link'])
        # item['intro'] = ''
        # item['abs'] = ''
        # item['content'] = response.text
        # item['purchaser'] = ''
        # item['create_time'] = str(datetime.datetime.now().strftime('%Y-%m-%d'))
        # item['proxy'] = ''
        # item['update_time'] = ''
        # item['deleted'] = ''
        # item['province'] = ''
        # item['base'] = ''
        # if 'tender' in item['link']:
        #     item['type'] = '招标公告'
        # if 'project' in item['link']:
        #     item['type'] = '基建项目'
        # item['items'] = ''
        # item['data_source'] = '00121'
        # item['end_time'] = ''
        # item['status'] = ''
        # item['serial'] = ''
        #
        # yield item
