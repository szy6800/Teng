import datetime
import json
import scrapy
import copy
from gansuxinwen.items import GansuxinwenItem
from gansuxinwen.tools.DB_mysql import *
from gansuxinwen.tools.re_time import Times
from gansuxinwen.tools.utils import Utils_
from gansuxinwen.tools.DB_redis import Redis_DB
import re

# http://www.gssgxy.cn/index/gzdt/index.html?page=1
# http://www.gssgxy.cn/index/hyzx/index.html?page=1

class GssgxySpider(scrapy.Spider):

    name = 'gssgxy'
    def __init__(self, *args, **kwargs):
        super(GssgxySpider, self).__init__()
        self.cates = [
            {"cate": "gzdt", "pages": 2},  # 招标公告
            {"cate": "hyzx", "pages": 2},  # 招标公告

        ]
        self.t = Times()
        self.c_time = datetime.datetime.utcnow() - datetime.timedelta(days=2)

    def start_requests(self):
        for each in self.cates:
            cate = each["cate"]
            pages = each["pages"]
            for p in range(1, pages):
                # p = f"_{p + 1}" if p else ""
                url = f"http://www.gssgxy.cn/index/{cate}/index.html?page={p}"
                # print(url)
                yield scrapy.Request(url=url, callback=self.parse, dont_filter=True)

    def parse(self, response, *args):
        count_list = response.xpath('//*[@class="news_box news_in_box"]/ul/li')
        if count_list is []:
            return
        for count in count_list:
            item = GansuxinwenItem()
        # 列表页链接和发布时间
            item['link'] = response.urljoin(count.xpath('./a/@href').get())
            item['title'] = count.xpath('.//h3/text()').get()
            if item['title'] is None:
                continue
            # 日
            day_time = count.xpath('.//a/div/span/text()').get()
            # 年月
            month_time = count.xpath('.//a/div/em/text()').get()
            pub_time = month_time+'-'+day_time
            PUBLISH = self.t.datetimes(pub_time)
            item['publish_time'] = PUBLISH.strftime('%Y-%m-%d')  # 发布
            # print(item['publish_time'],item['link'],item['title'])
            ctime = self.t.datetimes(item['publish_time'])
            if ctime < self.c_time:
                print('文章发布时间大于规定时间，不予采集', item['link'])
                return
            item['uid'] = 'zf' + Utils_.md5_encrypt(item['title'] + item['link'] + item['publish_time'])
            if Redis_DB().Redis_pd(item['uid']) is True:  # 数据去重
                print(item['title'], '\033[0;35m <=======此数据已采集=======> \033[0m')
                return
            item['province'] = '甘肃省'
            item['create_time'] = str(datetime.datetime.now().strftime('%Y-%m-%d'))
            item['data_source'] = '00668'
            item['status'] = ''
            item['base'] = ''
            yield scrapy.Request(item['link'], callback=self.parse_info, meta={'item': copy.deepcopy(item)},
                                 dont_filter=True)

    def parse_info(self, response):
        # print(response.url)
        if response.status != 200:
            return
        item = response.meta['item']
        author = re.findall('信息来源[:： \n]+(.*?)[\u2003]',response.text)[0]
        item['author'] = author
        # print(response.text)
        from lxml import etree
        html = etree.HTML(response.text)
        div_data = html.xpath('//*[@class="art_container"]')
        item['content'] = etree.tostring(div_data[0], encoding='utf-8').decode()
        yield item

