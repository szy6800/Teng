# -*- coding: utf-8 -*-
import scrapy
import copy
import time, re
from lxml import etree
from .test_text import type_polic

# 财务报表 http://m.wdfxw.net/pro1009Grade2QPage1.htm

class Wj2Spider(scrapy.Spider):
    name = 'py3'
    allowed_domains = ['hetong.110.com']
    start_urls = ['http://hetong.110.com/s?q=&a=c&ClassLevel2=&cid=20&f=0']
    # print(start_urls)

    def parse(self, response):
        item = {}
        list_url = response.xpath('//*[@class="searchruesult"]/ul/li/a/@href').getall()
        # 循环遍历
        for href in list_url:
            item['list_url'] = response.urljoin(href)
            yield scrapy.Request(item['list_url'], callback=self.parse_down, meta={'item': copy.deepcopy(item)})

    def parse_down(self, response):
        item = response.meta['item']
        listUrl = response.xpath('//*[@class="searchlist"]/ul/li/a/@href').getall()
        titles = response.xpath('//*[@class="searchlist"]/ul/li/a/text()').getall()

        for href, title in zip(listUrl, titles):
            item['url'] = response.urljoin(href)
            item['title'] = title
            # print(item['url'],item['img'],item['title'])
            yield scrapy.Request(item['url'], callback=self.parse_info, meta={'item': copy.deepcopy(item)})

    def parse_info(self, response):
        item = response.meta['item']
        html = etree.HTML(response.text)
        for elem in html.xpath('//style|//script|//*[@id="qrcode"]'):
            elem.getparent().remove(elem)
        content = html.xpath('//*[@id="articleBody"]//text()')
        sss = ''
        for i in content:
            sss = sss + i
        # 去除
        item['content'] = sss.strip()
        div_data = html.xpath('//*[@id="articleBody"]')
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
        contentHtml = etree.tostring(div_data[0], encoding='utf-8').decode()
        compal = re.compile('style=".*?"')
        contentHtml = re.sub(compal, '', contentHtml)
        try:
            tables = html.xpath('//*[@id="articleBody"]//table/@width')[0]
            item['contentHtml'] = re.sub(tables, '', contentHtml)
        except:
            item['contentHtml'] = re.sub(compal, '', contentHtml)

        item['type'] = type_polic(item)

        yield item












