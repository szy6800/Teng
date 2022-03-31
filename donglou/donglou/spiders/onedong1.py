import datetime
import json

import scrapy
import re
import time

from copy import deepcopy
from donglou.items import DonglouItem
from sqlalchemy import create_engine
import numpy as np
import pandas as pd

# def dbz():
#     # now = datetime.datetime.now()
#     # otherStyleTime = now.strftime("%Y-%m-%d")
#
#     sql1 = f'''SELECT id,county FROM `ershou`;'''
#     sql2 = f'''SELECT id,county FROM `ershouid`;'''
#     # print(sql)
#     engine = create_engine('mysql+pymysql://root:q!dwyyl6:q3L@127.0.0.1:3306/test?charset=utf8')
#     engine2 = create_engine('mysql+pymysql://root:q!dwyyl6:q3L@127.0.0.1:3306/test?charset=utf8')
#     df = pd.read_sql(sql1, engine)
#     df = df.drop_duplicates(subset=['id']) # 默认保留一条重复数据
#     # print(df)
#     df1 = pd.read_sql(sql2, engine2)
#     df1 = df1.drop_duplicates(subset=['id'])  # 默认保留一条重复数据
#     engine.dispose()
#     engine2.dispose()
#     # print(df1)
#     db2 = pd.concat([df, df1], axis=0, sort=False, ignore_index=True)
#     # print(db2)
#     dbz = db2.drop_duplicates(subset=['id'], keep=False)
#     # print(dbz)
#     print(f'对比保留了{len(dbz)}条')
#     dbz = dbz[['id','county']].values.tolist() # df转列表
#     # print(dbz)
#     return dbz

def lng_map(html):
    lng = re.search("resblockPosition:'(.*?)',", html).group(1)
    return lng

def id_map(html):
    lng = re.search("xiaoqu/(.*?)/", html).group(1)
    return lng

class OnedongSpider(scrapy.Spider):
    name = 'onedong'
    # allowed_domains = ['www.c']
    # start_urls = ['http://www.c/']

    def __init__(self, *args, **kwargs):
        super(OnedongSpider, self).__init__()
        self.cates = [
            {"cate": "xixianxinquxian", "pages": 3, 'xiaoqu_name':'陕西省|西安市|西咸新区（西安）'},
        ]
        # self.L = {'陕西省|西安市|碑林': 'https://xa.lianjia.com/xiaoqu/beilin/',
        #           '陕西省|西安市|未央': 'https://xa.lianjia.com/xiaoqu/weiyang/',
        #           '陕西省|西安市|灞桥': 'https://xa.lianjia.com/xiaoqu/baqiao/',
        #           '陕西省|西安市|新城区': 'https://xa.lianjia.com/xiaoqu/xinchengqu/',
        #           '陕西省|西安市|临潼': 'https://xa.lianjia.com/xiaoqu/lintong/',
        #           '陕西省|西安市|阎良': 'https://xa.lianjia.com/xiaoqu/yanliang/',
        #           '陕西省|西安市|长安': 'https://xa.lianjia.com/xiaoqu/changan7/',
        #           '陕西省|西安市|莲湖': 'https://xa.lianjia.com/xiaoqu/lianhu/',
        #           '陕西省|西安市|雁塔': 'https://xa.lianjia.com/xiaoqu/yanta/',
        #           '陕西省|西安市|蓝田': 'https://xa.lianjia.com/xiaoqu/lantian/',
        #           '陕西省|西安市|鄠邑区': 'https://xa.lianjia.com/xiaoqu/huyiqu/',
        #           '陕西省|西安市|周至': 'https://xa.lianjia.com/xiaoqu/zhouzhi/',
        #           '陕西省|西安市|高陵': 'https://xa.lianjia.com/xiaoqu/gaoling1/',
        #           '陕西省|西安市|西咸新区（西安）': 'https://xa.lianjia.com/xiaoqu/xixianxinquxian/'}

    def start_requests(self):
        for each in self.cates:
            cate = each["cate"]
            pages = each["pages"]
            k = each['xiaoqu_name']
            for p in range(1, pages):
                # p = f"_{p+1}" if p else ""
                url = f"https://xa.lianjia.com/xiaoqu/{cate}/pg{p}"
                yield scrapy.Request(url=url, callback=self.parse, dont_filter=True,meta={'k': k},)

    # def start_requests(self):
    #     for k, v in self.X.items():
    #         new_url = v
    #         # print(new_url)
    #         page = 25
    #         yield scrapy.Request(new_url, callback=self.parse, meta={'k': k, 'v': v, 'page': page})
    #         # for i in range(1,6):
    #         #     new_url = v + f'p{str(i)}'
    #         #     page = 1
    #         #     # time.sleep(1)
    #         #     yield scrapy.Request(new_url, callback=self.parse,meta={'k': k, 'v': v, 'i': i, 'page':page})
    #         #     # break
    def parse(self, response):

        k = response.meta['k']
        ssq = k.split('|')
        count_list = response.xpath('//li[@class="clear xiaoquListItem"]//div[@class="title"]/a')
        try:
            pa = response.xpath('/html/body/div[4]/div[1]/div[3]/div[2]/div/@page-data').get()
            len_pa = json.loads(pa)['totalPage']
        except:
            return
        for count in count_list:
            item = DonglouItem()
            title = count.xpath('./text()').get()
            x_url = count.xpath('./@href').get()
            item['arch_name'] = title
            item['arch_id'] = id_map(x_url)
            item['link'] = x_url
            item['prov_name'] = ssq[0]
            item['city_name'] = ssq[1]
            item['country_name'] = ssq[2]
            item['source_name'] = '链家'
            item['crawler_time'] = str(datetime.datetime.now().strftime('%Y-%m-%d'))
            # time.sleep(1)
            yield scrapy.Request(x_url, callback=self.son_parse,meta={'item': deepcopy(item)})

    def son_parse(self, response):
        item = response.meta['item']
        addr = response.xpath('//div[@class="detailDesc"]/text()').get()
        peice = response.xpath('//span[@class="xiaoquUnitPrice"]/text()').get()
        ng_list = lng_map(response.text).split(',')
        item['arch_add'] = addr
        item['avg_price'] = peice
        item['dispx'] = ng_list[0]
        item['dispy'] = ng_list[1]
        count_list = response.xpath('//div[@class="xiaoquInfoItem"]')
        for count in count_list:
            if count.xpath('./span[1]/text()').get() == '建筑类型':
                item['build_category'] = count.xpath('./span[2]/text()').get()
            if count.xpath('./span[1]/text()').get() == '物业费用':
                item['property_fee'] = count.xpath('./span[2]/text()').get()
            if count.xpath('./span[1]/text()').get() == '物业公司':
                item['property_company'] = count.xpath('./span[2]/text()').get()
            if count.xpath('./span[1]/text()').get() == '开发商':
                item['building_developers'] = count.xpath('./span[2]/text()').get()
            if count.xpath('./span[1]/text()').get() == '楼栋总数':
                item['building_number'] = count.xpath('./span[2]/text()').get()
            if count.xpath('./span[1]/text()').get() == '房屋总数':
                item['house_number'] = count.xpath('./span[2]/text()').get()
        # print(item)
        yield item
