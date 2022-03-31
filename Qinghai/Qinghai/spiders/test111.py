# -*- coding: utf-8 -*-

# @Author : 石张毅
# @Site :59医疗器械网 http://www.59med.com/news/list.php?catid=26
# @introduce： 招中标信息

import scrapy
import copy
from lxml import etree


class A59medSpider(scrapy.Spider):
    name = 'test'
    # allowed_domains = ['59med.com']
    start_urls = ['https://www.zjzhongtian.com/news/ann_details/1337.html']

    def parse(self, response, **kwargs):
        html = etree.HTML(response.text)
        div_data = html.xpath('string(//*[@class="conimg"])')
        # div_data = ''.join(html.xpath('//*[@class="conimg"]//text()'))
        # print(div_data)

        # 获取html标签
        div_data = html.xpath('//*[@class="con"]')[0]
        contentHtml = etree.tostring(div_data, encoding='utf-8').decode()
        print(contentHtml)




