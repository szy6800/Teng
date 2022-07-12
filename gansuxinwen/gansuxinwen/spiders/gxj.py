# -*- coding: utf-8 -*-

# @Time : 2022-07-11 18:16:36
# @Author : 石张毅
# @Site :http://gxj.lanzhou.gov.cn/col/col2703/index.html,
        # http://gxj.lanzhou.gov.cn/col/col2684/index.html
        # http://gxj.lanzhou.gov.cn/col/col2689/index.html
        # http://gxj.lanzhou.gov.cn/col/col2687/index.html
        # http://gxj.lanzhou.gov.cn/col/col2683/index.html
        # http://gxj.lanzhou.gov.cn/col/col2688/index.html
# @introduce: 兰州工业和信息化局
import scrapy
import copy
from gansuxinwen.items import GansuxinwenItem
from gansuxinwen.tools.DB_mysql import *
from gansuxinwen.tools.re_time import Times
from gansuxinwen.tools.utils import Utils_
from gansuxinwen.tools.DB_redis import Redis_DB
import re
import datetime
import scrapy


class GxjSpider(scrapy.Spider):
    name = 'gxj'

    def __init__(self, *args, **kwargs):
        super(GxjSpider, self).__init__()
        self.cates = [
            {"cate": "col2703", "pages": 2},
            {"cate": "col2684", "pages": 2},
            {"cate": "col2689", "pages": 2},
            {"cate": "col2687", "pages": 2},
            {"cate": "col2683", "pages": 2},
            {"cate": "col2688", "pages": 2},
        ]
        self.t = Times()
        self.c_time = datetime.datetime.utcnow() - datetime.timedelta(days=2)

    def start_requests(self):
        for each in self.cates:
            cate = each["cate"]
            # p = f"_{p + 1}" if p else ""
            url = f"http://gxj.lanzhou.gov.cn/col/{cate}/index.html"
            # print(url)
            yield scrapy.Request(url=url, callback=self.parse, dont_filter=True)

    def parse(self, response, *args):
        list_urls = re.findall("/art/.*\.html", response.text)
        titles = re.findall("title='(.*?)'>", response.text)
        pub_time = re.findall(">(\d{4}-\d{2}-\d{2})</td>", response.text)
        for href, title, pub_time in zip(list_urls, titles, pub_time):
            item=GansuxinwenItem()
            # print(response.urljoin(href))
            item['link'] = response.urljoin(href.strip())
            item['title'] = title.strip()
            if item['title'] is None:
                continue
            PUBLISH = self.t.datetimes(pub_time)
            item['publish_time'] = PUBLISH.strftime('%Y-%m-%d')
            item['uid'] = 'zf' + Utils_.md5_encrypt(item['title'] + item['link'] + item['publish_time'])
            ctime = self.t.datetimes(item['publish_time'])
            if ctime < self.c_time:
                print('文章发布时间大于规定时间，不予采集', item['link'])
                return
            if Redis_DB().Redis_pd(item['uid']) is True:  # 数据去重
                print(item['uid'], '\033[0;35m <=======此数据已采集=======> \033[0m')
                return
            item['province'] = '甘肃省|兰州市'
            item['create_time'] = str(datetime.datetime.now().strftime('%Y-%m-%d'))
            item['data_source'] = '00669'
            item['status'] = ''
            item['base'] = ''
            item['author'] = '兰州市工业和信息化局'
            # print(item['link'], item['publish_time'],item['title'])
            yield scrapy.Request(item['link'], callback=self.parse_info, meta={'item': copy.deepcopy(item)},dont_filter=True)


    def parse_info(self, response):
        # print(response.url)
        if response.status != 200:
            return
        item = response.meta['item']
        # author = re.findall('信息来源[:： \n]+(.*?)[\u2003]',response.text)[0]
        from lxml import etree
        html = etree.HTML(response.text)
        div_data = html.xpath('//*[@id="zoom"]')
        item['content'] = etree.tostring(div_data[0], encoding='utf-8').decode()
        yield item
