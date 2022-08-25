# -*- coding: utf-8 -*-
import scrapy

import time
import re
from lxml import etree
import copy

from .test import *

 # 加盟公司信息 https://www.admin5.com/browse/130/list_50.shtml

class WjSpider(scrapy.Spider):
    name = 'wj7'
    allowed_domains = ['admin5.com']
    start_urls = ['https://xm.admin5.com/list-{}.html'.format(i) for i in range(1,51)]  # 7

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
        list_url = response.xpath('//*[@class="clear_fix bg1"]/a[1]/@href').getall()
        for href in list_url:
            item['url'] = response.urljoin(href.strip())
            yield scrapy.Request(item['url'], callback=self.parse_info, meta={'item': copy.deepcopy(item)}, dont_filter=True)

    def parse_info(self, response):
        item = response.meta['item']
        # 标题
        item['title'] = response.xpath('//*[@class="details-title"]/h2/text()').get()

        item['company'] = response.xpath('//*[@class="details-title"]/p/text()').get()

        address = response.xpath("//*[contains(text(),'公司地址：')]/text()").get()
        item['address'] = process(address)

        industry = response.xpath("//*[contains(text(),'所属行业：')]/text()").get()
        item['industry'] = process(industry)

        html = etree.HTML(response.text)
        for elem in html.xpath('//style|//script|//*[@class="ad-banquan"]|//*[@class="content-ad"]|//*[@class="ad-text"]'):
            elem.getparent().remove(elem)
        content1 = html.xpath('//*[@id="about"]//text()')
        sss = ''
        for i in content1:
            sss = sss + i
        # 去除
        item['ProjectIntroduction'] = sss.strip()
        div_data = html.xpath('//*[@id="about"]')
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
        item['ProjectIntroductionHtml'] = etree.tostring(div_data[0], encoding='utf-8').decode()

        content2 = html.xpath('//*[@id="team"]//text()')
        sss = ''
        for i in content2:
            sss = sss + i
        # 去除
        item['ProjectAdvantages'] = sss.strip()
        div_data = html.xpath('//*[@id="team"]')
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
        item['ProjectAdvantagesHtml'] = etree.tostring(div_data[0], encoding='utf-8').decode()
        #
        yield item



