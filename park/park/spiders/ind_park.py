# -*- coding: utf-8 -*-

# @Time : 2022-09-02 11:40:06
# @Author : 石张毅
# @Site :  https://y.qianzhan.com/system/index/
# @introduce: 前瞻产业园区库
import hashlib
import json
import copy
import re
from park.spiders.ind import ind
import scrapy


class IndParkSpider(scrapy.Spider):
    name = 'ind_park'

    def __init__(self, *args, **kwargs):
        super(IndParkSpider, self).__init__()
        self.ind = ind()

    def start_requests(self):
        for i in range(0, 30):# 3101
            url = f'https://y.qianzhan.com/system/GetTableData2?page=1&pageSize=20&queryStr=&level=1&NodeType=1&Node1=3101&Node2=&Node3=&Node4=&match=0&agg=1&sort=&way=desc'
            yield scrapy.Request(url=url, callback=self.parse, dont_filter=True, meta={'industry':ind})

    def parse(self, response, *args, **kwargs):
        json_text = json.loads(response.text)
        count_list = json_text['list']
        for count in count_list:
            item = dict()
            item['title'] = count['y_name']
            link = count['y_uid']
            item['link'] = f'https://y.qianzhan.com/yuanqu/item/{link}.html'
            # item['industry'] = response.meta['industry']
            item['industry'] = '全部'
            item['purchase'] = str(count['y_buyed'])
            item['province'] = count['y_province']
            item['city'] = count['y_city']
            item['county'] = count['y_district']
            item['is_coo'] = ''
            item['area'] = str(count['y_area'])
            item['comp_num'] = str(count['y_comps'])
            item['price'] = str(count['y_price'])
            # 去重
            uid = item['title']+item['province']+item['city']+item['county']+link
            item['uid'] = hashlib.md5(uid.encode(encoding='utf-8')).hexdigest()

            yield scrapy.Request(item['link'], callback=self.parse_info,
                                 meta={'item': copy.deepcopy(item),},
                                 dont_filter=True)

    def parse_info(self, response):
        # print(response.text)
        if response.status != 200:
            return
        item = response.meta['item']
        item['address'] = response.xpath('//*[@class="line2"]/p[1]/text()').get().strip().replace('本数据来自前瞻产业研究院产业园区数据库，前瞻产业研究院20年持续聚焦全国细分产业研究、产业规划、产业园区规划、产业地产规划、特色小镇规划、产业新城规划及产业园区招商引资等，助力地方产业发展，促进产城融合。','')
        lngs = response.xpath('//*[@id="iGMap"]/@src').get()
        lngs1 = re.findall('\?center=(.*?)&zoom',lngs)[0]
        item['lng'] = lngs1.split(',')[0]
        item['lat'] = lngs1.split(',')[1]
        yield item


