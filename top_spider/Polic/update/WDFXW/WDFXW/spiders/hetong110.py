# -*- coding: utf-8 -*-
import requests
import scrapy
import copy
import time, re
from lxml import etree

class Wj2Spider(scrapy.Spider):
    name = 'hetongtong110'
    allowed_domains = ['hetong.110.com']

    start_urls = ['http://hetong.110.com/s?q=&a=c&tid=0&cid=26&rid=0&f=0&sp=0&ep=0&p={}&oq='.format(i) for i in range(1,11)]

    def parse(self, response):
        item = {}
        list_url = response.xpath('//*[@class="searchlist"]/ul/li/a/@href').getall()
        titles = response.xpath('//*[@class="searchlist"]/ul/li/a/text()').getall()

        # 循环遍历
        for href, title in zip(list_url, titles):
            # 原始链接
            item['url'] = response.urljoin(href)

            item['title'] = title
            yield scrapy.Request(item['url'], callback=self.parse_down, meta={'item': copy.deepcopy(item)})

    def parse_down(self, response):
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

        item['type'] = '经销合同'

        yield item
