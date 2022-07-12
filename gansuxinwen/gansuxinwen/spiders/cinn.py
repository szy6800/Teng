
import datetime
import json
import scrapy
import copy
from gansuxinwen.items import GansuxinwenItem
from gansuxinwen.tools.DB_mysql import *
from gansuxinwen.tools.re_time import Times
from gansuxinwen.tools.utils import Utils_
from gansuxinwen.tools.DB_redis import Redis_DB
# https://www.cinn.cn/

class CinnSpider(scrapy.Spider):
    name = 'cinn'
    def __init__(self, *args, **kwargs):
        super(CinnSpider, self).__init__()
        self.L = {
        }
        self.t = Times()
        self.c_time = datetime.datetime.utcnow() - datetime.timedelta(days=2)

    def start_requests(self):
        for p in range(2):
            p = f"_{p}" if p else ""
            new_url = f'http://www.cinn.cn/homeAjax_318{p}.html'
            yield scrapy.Request(new_url, callback=self.parse)

    def parse(self, response, *args):
        count_list = response.xpath('//*[@class="layCont_box_main_new"]/div')
        if count_list is []:
            return
        for count in count_list:
            item = GansuxinwenItem()
        # 列表页链接和发布时间
            item['link'] = count.xpath('./a/@href').get()
            item['title'] = count.xpath('.//h3/text()').get()
            if item['title'] is None:
                continue
            pub_time = count.xpath('.//p[1]/text()').get().replace('年','-').replace('月','-').replace('日','')
            PUBLISH = self.t.datetimes(pub_time)
            item['publish_time'] = PUBLISH.strftime('%Y-%m-%d')  # 发布
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
            item['author'] = '中国工业新闻网'
            item['data_source'] = '00667'
            item['status'] = ''
            item['base'] = ''
            yield scrapy.Request(item['link'], callback=self.parse_info, meta={'item': copy.deepcopy(item)},
                                 dont_filter=True)

    def parse_info(self, response):
        # print(response.url)
        if response.status != 200:
            return
        item = response.meta['item']
        # print(response.text)
        from lxml import etree
        html = etree.HTML(response.text)
        div_data = html.xpath('//*[@class="layCont_box_main_cont"]')
        item['content'] = etree.tostring(div_data[0], encoding='utf-8').decode()
        yield item


