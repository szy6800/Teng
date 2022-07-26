# -*- coding: utf-8 -*-

# @Author : 石张毅
# @Site :黄河上游水电开发有限公司  http://www.hhsd.com.cn/news/zx/?&category=1
# @introduce:

import scrapy
import copy
from Qinghai.tools.utils import Utils_
from Qinghai.tools.DB_mysql import *
from Qinghai.tools.re_time import Times
import datetime
from Qinghai.tools.uredis import Redis_DB

class HhsdSpider(scrapy.Spider):
    name = 'hhsd'
    allowed_domains = ['hhsd.com']
    start_urls = ['http://hhsd.com/']
    custom_settings = {
        'COOKIES_ENABLED':False,
        'DEFAULT_REQUEST_HEADERS': {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Cookie": "ARzami5PV4uxS=5hQv9tz0msH5hS.Zob5d.E757_hZ_Y0Sj7OyjJEsiHR4T839u9FNUWGRyzLvyukmENH7cpVGTJSky7l8Qvzu3wa; ARzami5PV4uxT=U31FZQ7qcBPhpJa_feZBOb12spiSVPysVQXdlvODvn1dGr9q1V1IRr3C5MdhLapqqdwPFrAqJb23xYKPOy0GnnbLl7Y6BCagy7_XkgUE7zPM85o9GhmwJssaBH83g5ILNw7TfPJZWYk2_tFmaRAFShTVdCPLwCSmuHHsuxkoEuMnfThRwE1ligmANGI0OZ2dPBbQ2H2HcxbSx6aASkylwwOK.cdx.MZ0W0_tkyr3q4hQx5omUG4oj24pp8cRCxf9kOz9BlpZE9uq.9WSWaI6by5QznKlx5lU6xK9b8GgDETMP4nQ6fJj02xlojR9wbBr5EP_hUDjh4tzQs_oPASCa1CmtsckI7R4_I6.hzVS5Va",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36",
        }
    }

    def __init__(self, *args, **kwargs ):
        super(HhsdSpider, self).__init__()
        self.cates = [
            {"cate": "zbgg", "pages": 2},  # 招标公告
        ]
        self.t = Times()
        self.c_time = datetime.datetime.utcnow() - datetime.timedelta(days=200)

    def start_requests(self):
        for each in self.cates:
            cate = each["cate"]
            pages = each["pages"]
            for p in range(1, pages):
                # p = f"_{p+1}" if p else ""
                url = f"http://www.hhsd.com.cn/news/zx/?&category=2&page=1"
                yield scrapy.Request(url=url, callback=self.parse,dont_filter=True)

    def parse(self, response):
        # print(response.text)
        item = {}
        # 列表页链接和发布时间
        list_url = response.xpath('//*[@class="m-news jsNews"]/ul/li/a/@href').getall()
        # print(list_url)
        titles = response.xpath('//*[@class="m-news jsNews"]/ul/li/a/span/text()').getall()
        # print(titles)
        pub_times = response.xpath('//*[@class="m-news jsNews"]/ul/li/a/span/following::b[1]/text()').getall()
        #循环遍历

        for href, title, pub_time in zip(list_url, titles, pub_times):
            # print(response.urljoin(href))
            item['link'] = response.urljoin(href.strip())
            item['title'] = title.strip()
            if item['title'] is None:
                continue
            # pub_time = re.findall('\\d{4}-\\d{2}-\\d{2}', pub_time)[0]
            PUBLISH = self.t.datetimes(pub_time)
            item['publish_time'] = PUBLISH.strftime('%Y-%m-%d')  # 发布时间
            item['uid'] = 'zf' + Utils_.md5_encrypt(item['title'] + item['link'] + item['publish_time'])
            if Redis_DB().Redis_pd(item['uid']) is True:  # 数据去重
                print(item['uid'], '\033[0;35m <=======此数据已采集=======> \033[0m')
                return
            ctime = self.t.datetimes(item['publish_time'])
            if ctime < self.c_time:
                print('文章发布时间大于规定时间，不予采集', item['link'])
                return
            yield scrapy.Request(item['link'], callback=self.parse_info, meta={'item': copy.deepcopy(item)},dont_filter=True)

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
        div_data = html.xpath('//*[@class="content-p"]')
        item['content'] = etree.tostring(div_data[0], encoding='utf-8').decode()
        # 购买人
        item['purchaser'] = ''
        item['create_time'] = str(datetime.datetime.now().strftime('%Y-%m-%d'))
        # 代理人
        item['proxy'] = ''
        item['update_time'] = ''

        item['deleted'] = ''
        # 省 份
        item['province'] = ''
        # 基础
        item['base'] = ''

        item['type'] = ''

        # 行业
        item['items'] = ''
        # 类型编号
        item['data_source'] = '00160'
        item['end_time'] = ''
        item['status'] = ''
        # 采购编号
        item['serial'] = ''

        yield item
