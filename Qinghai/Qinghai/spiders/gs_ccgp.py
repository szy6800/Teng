# -*- coding: utf-8 -*-

# @Time : 2022-08-18 17:04:17
# @Author : 石张毅
# @Site : http://www.ccgp-gansu.gov.cn/web/doSearchmxarticlelssj.action?limit=20&start=0
# @introduce: 甘肃政府采购网


import scrapy
import copy
from Qinghai.tools.utils import Utils_
from Qinghai.tools.DB_mysql import *
from Qinghai.tools.re_time import Times
import datetime
import jsonpath
import json
import re
from Qinghai.tools.uredis import Redis_DB

class GsCcgpSpider(scrapy.Spider):
    name = 'gs_ccgp'

    custom_settings = {
        'COOKIES_ENABLED': False,
        'DEFAULT_REQUEST_HEADERS': {
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Cookie": '4hP44ZykCTt5S=5Jqk4uTfMdcm21mdg5zxMeKWfjJwK.e6UwVuKMpIp5VOTIyDDDL24XeK7YE4ALfgFWJOY24nBRSVBlK_eog07kG; JSESSIONID=6A764516960DD9335ADC19BE0E8D76C4.tomcat2; 4hP44ZykCTt5T=feh_DBoWyuXiHXIB.SJIL8Ip3MeWcjVaUDK1vm2rNJBCw6aZY8aQLyDbCdCb4t97y8gv7CcGEmOiO4R8_z01vavwXbXk0znhH5jEi9d.D6_6nHZ091cOrjHRuvapXaWbvaR8edHnrWRjFtzeV4M_VWKDSozHv3L9A7Jx_0V0gVJj75.Ysz7gt4oThm9yEyTA79A1qnjtRTV5NKqehHrg6BCKBQLx7MyZkGPb3p054OHhCqUe9B7WbbIersqyzoM5mS26J3cKi9UomE6LGUYNUbrOb4RPpGXd_FAd8APnSr4eeRTlBvI7V40WFqIppBCGF4uPVRjFMIoXpbrxnnNCoqEt92Fzs7GTmCat_OGVsna',
            "Host": "www.ccgp-gansu.gov.cn",
            "Pragma": "no-cache",
            "Referer": "http://www.ccgp-gansu.gov.cn/web/doSearchmxarticlelssj.action?limit=20&start=120",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36",
        }
    }

    def __init__(self, *args, **kwargs):
        super(GsCcgpSpider, self).__init__()
        self.t = Times()
        self.c_time = datetime.datetime.utcnow() - datetime.timedelta(days=7)

    def start_requests(self):
        for i in range(100,130,20):

            url = f"http://www.ccgp-gansu.gov.cn/web/doSearchmxarticlelssj.action?limit=20&start={i}"
            # url = f'http://www.ccgp-gansu.gov.cn/web/doSearchmxarticlelssj.action?limit=20&start={i}'
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response, **kwargs):
        count_list = response.xpath('//*[@class="Expand_SearchSLisi"]/li')
        if count_list is []:
            return
        for count in count_list:
            item = dict()
            # 列表页链接和发布时间
            item['link'] = response.urljoin(count.xpath('./a/@href').get())
            item['title'] = count.xpath('./a/text()').get()
            if item['title'] is None:
                continue
            # 大数据集合
            con = count.xpath('./p[1]/span/text()').get()
            pub_time = re.findall('发布时间[:： \n]+(.*?)[\|\s*]', con)[0]
            PUBLISH = self.t.datetimes(pub_time)
            item['publish_time'] = PUBLISH.strftime('%Y-%m-%d')  # 发布时间
            # 代理机构
            item['proxy'] = re.findall('代理机构[:： \n]+(.*?)[\|\s*]', con)[0]
            # 采购人
            item['purchaser'] = re.findall('采购人[:： \n]+(.*?)[\|\s*]', con)[0]
            con1 = count.xpath('./p[2]/span/strong/text()').get()
            # 行业
            item['items'] = con1.split('|')[2].strip()
            # 分类
            item['type'] = con1.split('|')[0].strip()
            item['uid'] = 'zf' + Utils_.md5_encrypt(item['title'] + item['link'] + item['publish_time'])
            ctime = self.t.datetimes(item['publish_time'])
            if ctime < self.c_time:
                print('文章发布时间大于规定时间，不予采集', item['link'])
                return
            if Redis_DB().Redis_pd(item['uid']) is True:  # 数据去重
                print(item['uid'], '\033[0;35m <=======此数据已采集=======> \033[0m')
                continue
            yield scrapy.Request(item['link'], callback=self.parse_info, meta={'item': copy.deepcopy(item)},
                                 dont_filter=True)
    #
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
        div_data = html.xpath('//*[@id="fontzoom"]')
        item['content'] = etree.tostring(div_data[0], encoding='utf-8').decode()
        item['create_time'] = str(datetime.datetime.now().strftime('%Y-%m-%d'))
        item['update_time'] = ''
        item['deleted'] = ''
        item['province'] = '甘肃省'
        item['base'] = ''
        item['data_source'] = '00759'
        item['end_time'] = ''
        item['status'] = ''
        item['serial'] = ''
        # print(item)
        yield item


