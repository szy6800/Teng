# -*- coding: utf-8 -*-
import scrapy

import time
import re
from lxml import etree
import copy,json,jsonpath
from .wj_text import type_polic,index

 # 创业问答 http://www.cdshe.com/q-237.html

class WjSpider(scrapy.Spider):
    name = 'wj5'
    allowed_domains = ['www.cdshe.com']
    # start_urls = ['http://qncye.com/baodao/hangye/list_17_{}.html'.format(i) for i in range(1,5)]  # 7

    def start_requests(self):
        url = 'http://www.cdshe.com/question/newquestionmore'
        # FormRequest 是Scrapy发送POST请求的方法
        yield scrapy.FormRequest(
            url=url,
            formdata={"page": "4",},
            callback=self.parse
        )

    def parse(self, response):
        item = {}
        text = json.loads(response.text)
        list_url = jsonpath.jsonpath(text, '$..url')
        # 循环遍历
        for href in list_url:
            item['url'] = response.urljoin(href.strip())
            yield scrapy.Request(item['url'], callback=self.parse_info, meta={'item': copy.deepcopy(item)},
                                 dont_filter=True)

    def parse_info(self, response):
        item = response.meta['item']
        # 标题
        item['title'] = response.xpath('//*[@class="questiontitle"]/text()').get().strip()

        item['type_id'] = '1'
        html = etree.HTML(response.text)

        for elem in html.xpath('//style|//script'):
            elem.getparent().remove(elem)
        content = html.xpath('//*[@class="answerbox"]/div[1]//*[@class="answer-concent"]//text()')
        sss = ''
        for i in content:
            sss = sss + i
        # 去除
        item['answer'] = sss.strip()
        div_data = html.xpath('//*[@class="answerbox"]/div[1]//*[@class="answer-concent"]')
        p_list = div_data[0].xpath('.//*')
        # 遍历所有p标签，讲里边的src,oldsrc属性拼接上前半部分
        for p in p_list:
            try:
                scr_data = p.xpath('.//@src')[0]
                p.attrib['src'] = response.urljoin(scr_data)
            except:
                pass
            try:
                scr_data1 = p.xpath('.//@href')[0]
                p.attrib['href'] = response.urljoin(scr_data1)
            except:
                pass
        # # 将新的正文标签转成str保存
        item['answer_html'] = etree.tostring(div_data[0], encoding='utf-8').decode()

        yield item



