# -*- coding: utf-8 -*-
import json

import jsonpath
import scrapy
import time
import re
from lxml import etree
import copy
# http://rsj.hefei.gov.cn/zxzx/tzgg/index.html

class WjSpider(scrapy.Spider):
    name = 'IOS'
    allowed_domains = ['rsj.hefei.gov.cn']

    def start_requests(self):
        cate = [
            'eyJ2IjoiNzAzMjQ4OTcxMjQ5NzQ1OTIwOCIsImkiOjU0MH0=',
            'eyJ2IjoiNzAzMjQ4OTcxMjQ5NzQ1OTIwOCIsImkiOjU4MH0=',
            'eyJ2IjoiNzAzMjQ4OTcxMjQ5NzQ1OTIwOCIsImkiOjYwMH0=',
            'eyJ2IjoiNzAzMjUyNTc0ODY4NjU1MzA5NSIsImkiOjY0MH0=',
        ]

        for i in cate:
        #循环135页
        #构建post请求参数
            data = {"id_type":2,"sort_type":200,"cate_id":"6809635626879549454","tag_id":"6809640400832167949","cursor":i,"limit":20}
        #发送post请求
            yield scrapy.FormRequest(
                url = 'https://api.juejin.cn/recommend_api/v1/article/recommend_cate_tag_feed?aid=2608&uuid=7003543927303341582',
                method='POST',
                body=json.dumps(data),
                headers={'Content-Type': 'application/json'},
                callback = self.parse)

    def parse(self, response):
        item = {}
        text = json.loads(response.text)
        article_id = jsonpath.jsonpath(text, '$..article_info.article_id')
        coverImgUrl  = jsonpath.jsonpath(text, '$..article_info.cover_image')
        articleTitle = jsonpath.jsonpath(text, '$..article_info.title')
        articleDesc = jsonpath.jsonpath(text, '$..article_info.brief_content')
        for article_id, coverImgUrl, articleTitle, articleDesc in zip(article_id,coverImgUrl,articleTitle,articleDesc):
            item['contentUrl'] = 'https://juejin.cn/post/'+article_id
            item['coverImgUrl'] = coverImgUrl
            item['articleTitle'] = articleTitle
            item['articleDesc'] = articleDesc

            # print(item['contentUrl'],item['coverImgUrl'],item['articleTitle'],item['articleDesc'])

            yield scrapy.Request(item['contentUrl'], callback=self.parse_info, meta={'item': copy.deepcopy(item)},dont_filter=True)


    def parse_info(self, response):

        item= response.meta['item']
        item['contentHtml'] = re.findall('.+mark_content:([\s\S.]+),author_user_info', response.text)[0]
        item['type'] = 'ios'

        yield item

