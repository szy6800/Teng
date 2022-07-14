# -*- coding: utf-8 -*-

# @Time : 2022-07-13 17:19:13
# @Author : 石张毅
# @Site :
# @introduce:

import re
import datetime
import json
import copy
from gansuxinwen.items import GansuxinwenItem
from gansuxinwen.tools.DB_mysql import *
from gansuxinwen.tools.re_time import Times
from gansuxinwen.tools.utils import Utils_
from gansuxinwen.tools.DB_redis import Redis_DB
import scrapy


class MiitSpider(scrapy.Spider):

    name = 'miit'
    def __init__(self, *args, **kwargs):
        super(MiitSpider, self).__init__()
        self.cates = [
            {"pageid": "6333578be1d646aabc3e0e79406688c9", "pages": 2,},  # 招6标公告
            {"pageid": "d3e2bede1bc045e2875fc7161c01db7d", "pages": 2,},  # 招6标公告
            {"pageid": "028da85b0dbd4c9cb96fd5f421cd32b8", "pages": 2,},  # 招6标公告
            {"pageid": "e4d6c56063fa4edca257cc2e24ad473c", "pages": 2,},  # 招6标公告


        ]
        self.t = Times()
        self.c_time = datetime.datetime.utcnow() - datetime.timedelta(days=2)

    def start_requests(self):
        for each in self.cates:
            pageid = each["pageid"]
            pages = each["pages"]
            for p in range(1, pages):
                # p = f"_{p}" if p else ""
                url = f"https://www.miit.gov.cn/api-gateway/jpaas-publish-server/front/page/build/unit?webId=8d828e408d90447786ddbe128d495e9e&pageId={pageid}&parseType=buildstatic&pageType=column&tagId=%E5%8F%B3%E4%BE%A7%E5%86%85%E5%AE%B9&tplSetId=209741b2109044b5b7695700b2bec37e&paramJson=%7B%22pageNo%22%3A{p}%2C%22pageSize%22%3A%2224%22%7D"
                yield scrapy.Request(url=url, callback=self.parse, dont_filter=True)

    def parse(self, response, *args):
        json_text = json.loads(response.text)
        # print(json_text)
        htmls = json_text['data']['html']
        from lxml import etree
        html = etree.HTML(htmls)
        count_list = html.xpath('//*[@class="page-content"]/ul/li')
        # print(count_list)
        #
        if count_list is []:
            return
        for count in count_list:
            item = GansuxinwenItem()
            # 列表页链接和发布时间
            item['link'] = response.urljoin(count.xpath("./a/@href")[0])
            # print(item['link'])
            item['title'] = count.xpath("./a/@title")[0]
            if item['title'] is None:
                continue
            pub_time = count.xpath('./span/text()')[0]
            PUBLISH = self.t.datetimes(pub_time)
            item['publish_time'] = PUBLISH.strftime('%Y-%m-%d')  # 发布
            print(item['publish_time'],item['link'],item['title'])
            ctime = self.t.datetimes(item['publish_time'])
            if ctime < self.c_time:
                print('文章发布时间大于规定时间，不予采集', item['link'])
                return
            item['uid'] = 'zf' + Utils_.md5_encrypt(item['title'] + item['link'] + item['publish_time'])
            if Redis_DB().Redis_pd(item['uid']) is True:  # 数据去重
                print(item['title'], '\033[0;35m <=======此数据已采集=======> \033[0m')
                return
            item['province'] = ''
            item['create_time'] = str(datetime.datetime.now().strftime('%Y-%m-%d'))
            item['data_source'] = '00678'
            item['status'] = ''
            item['base'] = ''
            yield scrapy.Request(item['link'], callback=self.parse_info, meta={'item': copy.deepcopy(item)},
                                 dont_filter=True)

    def parse_info(self, response):
        # print(response.text)
        if response.status != 200:
            return
        item = response.meta['item']
        try:
            author = re.findall('来源[:： \n]+(.*?)<', response.text)[0]
            item['author'] = author
        except:
            item['author'] = '中华人民共和国工业和信息部'
        # print(response.text)
        from lxml import etree
        html = etree.HTML(response.text)
        div_data = html.xpath('//*[@id="con_con"]')
        item['content'] = etree.tostring(div_data[0], encoding='utf-8').decode()
        # print(item)
        yield item

