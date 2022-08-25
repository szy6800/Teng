# -*- coding: utf-8 -*-
import scrapy

import time
import re
from lxml import etree
import copy
from .wj_text import type_polic,index

 #金税四期 https://www.acc5.com/search.php?word=%E9%87%91%E7%A8%8E%E5%9B%9B%E6%9C%9F&type=news&page=4

class WjSpider(scrapy.Spider):
    name = 'wj2'
    allowed_domains = ['qncye.com']

    start_urls = ['https://www.acc5.com/search.php?word=%E9%87%91%E7%A8%8E%E5%9B%9B%E6%9C%9F&type=news&page={}'.format(i) for i in range(1,7)]  # 7
    # start_urls = ['http://bj.renrenbang.com/gszc/?tf=f&p={}'.format(i) for i in range(1,5)]  #
    # # start_urls = ['http://bj.renrenbang.com/zhishichanquan/?tf=f&p={}'.format(i) for i in range(1,2)]  #

    # def start_requests(self):
    #     for each in index():
    #         cate = each["cate"]
    #         pages = each["pages"]
    #         for p in range(pages):
    #             p = f"{p}" if p else ""
    #             url = f"http://bj.renrenbang.com/{cate}/?tf=f&p={p}"
    #             yield scrapy.Request(url=url, callback=self.parse, dont_filter=True)

    def parse(self, response):
        item = {}
        list_url = response.xpath('//*[@class="row"]//a/@href').getall()
        # print(list_url)
        # 循环遍历
        for href in list_url:
            # print(response.urljoin(href))
            item['url'] = response.urljoin(href.strip())
            yield scrapy.Request(item['url'], callback=self.parse_info, meta={'item': copy.deepcopy(item)},
                                 dont_filter=True)

    def parse_info(self, response):
        item = response.meta['item']
        # 标题
        item['title'] = response.xpath('//h1/text()').get().strip()

        item['type_id'] = 4
        html = etree.HTML(response.text)

        for elem in html.xpath('//style|//script'):
            elem.getparent().remove(elem)
        content = html.xpath('//*[@class="article-content"]//text()')
        sss = ''
        for i in content:
            sss = sss + i
        # 去除
        item['answer'] = sss.strip()
        div_data = html.xpath('//*[@class="article-content"]')
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


