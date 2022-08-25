# -*- coding: utf-8 -*-
import scrapy
import time
import re
from lxml import etree
import copy
from .msBureau import type_polic,index
import htmlmin
# http://kjj.guiyang.gov.cn/zfxxgk/fdzdgknr/tzgg/index_1.html


class GovSpider(scrapy.Spider):
    name = 'te'
    start_urls = ['https://www.jb51.cc/android/']

    def parse(self, response, *args):
        # print(response.text)
        list_url = response.xpath('//*[@class="title"]/a/@href').getall()
        # 去除最后一个
        #循环遍历
        for href in list_url[1:20]:
            url = response.urljoin(href.strip())
            # print(item['url'])
            yield scrapy.Request(url, callback=self.parse_info,
                                 dont_filter=True)

    def parse_info(self, response):
        html = etree.HTML(response.text)
        for elem in html.xpath('//*[@style="height:120px;margin-top:20px;"]|//*[@class="list-group"]|//*[@class="adsbygoogle"]|//*[@class="medium-zoom-image"]|//h2[contains(text(),"总结")]/following::p[1]|//h2[contains(text(),"总结")]/following::p[2]|//h2[contains(text(),"总结")]|//*[@class="alert alert-info"]'):
            elem.getparent().remove(elem)
        div_data = html.xpath('//*[@class="article-content"]')
        p_list = div_data[0].xpath('.//*')
        # 遍历所有p标签，讲里边的src,oldsrc属性拼接上前半部分
        for p in p_list:
            try:
                scr_data = p.xpath('.//@src')[0]
                p.attrib['src'] = response.urljoin(scr_data)
            except:
                pass
        # # 将新的正文标签转成str保存
        markdownContent = etree.tostring(div_data[0], encoding='utf-8').decode().replace('https://www.jb51.cc/pay.jpg','')
        title = response.xpath('//*[@class="article-title"]/h1/text()').get()
        item = {"title":title,
                "directory":"[]",
                "contentType":"MARKDOWN",
                "htmlContent":'',
                "headImg":"[]",
                "draft":"",
                "markdownContent":markdownContent,
                "tagIds":[1042842],
                "originalTitle":"",
                "originalUrl":"",
                "originalAuthor":""}
        yield item


