# -*- coding: utf-8 -*-

import json
import scrapy
import copy
import time,jsonpath
from lxml import etree
from .xa_text1 import index,type_polic
import re

class WuMakeSpider(scrapy.Spider):
    name = 'type2'
    allowed_domains = ['xiongan.gov.cn']

    def start_requests(self):
        for each in index():
            cate = each["cate"]
            pages = each["pages"]
            for p in range(pages):
                p = f"{p+1}" if p else ""
                url = f"http://da.wa.news.cn/nodeart/page?nid={cate}&pgnum={p}"
                yield scrapy.Request(url=url, callback=self.parse)

    #解析列表页
    def parse(self, response):
        text = json.loads(response.text)
        item = {}
        list_url = jsonpath.jsonpath(text, '$..LinkUrl')
        PubTime = jsonpath.jsonpath(text, '$..PubTime')
        Titles = jsonpath.jsonpath(text, '$..Title')
        SourceNames = jsonpath.jsonpath(text, '$..SourceName')
        for url, Ptime, title,SourceName in zip(list_url,PubTime,Titles,SourceNames):
            item['url'] = response.urljoin(url)
            item['title'] = title
            item['sourceSite'] = SourceName
            timeArray = time.strptime(Ptime, "%Y-%m-%d %H:%M:%S")
            timeStamp = int(time.mktime(timeArray)) * 1000
            item['publishTime'] = timeStamp
            yield scrapy.Request(item['url'], callback=self.parse_info, meta={'item': copy.deepcopy(item)})

    #解析详情
    def parse_info(self, response):
        item = response.meta['item']
        #城市
        item['city'] = 10
        #城市id
        item['cityId'] = ''
        #主题
        item['subject'] = ''
        #主题_id
        item['classifyId'] = 7
        #大分类
        item['big_type'] = ''
        # 大分类_id
        item['administrativeId'] = ''
        # 正文
        #去除js和css节点
        html = etree.HTML(response.text)
        for elem in html.xpath('//style|//script'):
            elem.getparent().remove(elem)
        content = html.xpath('//*[@class="main-content-box"]//text()|//*[@class="main"]//text()|//*[@class="con"]//text()')
        sss = ''
        for i in content:
            sss = sss + i
        #去除
        item['content'] =sss.strip()
        # 解析html
        try:
            # 获取正文标签
            div_data = html.xpath('//*[@class="con"]|//*[@class="main-content-box"]')
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
            compal = re.compile('face=".*?"|FONT-FAMILY: 微软雅黑')
            item['contentHtml'] = re.sub(compal, '', contentHtml)
        except:
            for elem in html.xpath('//h1|//*[@class="m-info domMobile"]'):
                elem.getparent().remove(elem)
            div_data = html.xpath('//*[@class="main"]')
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
            compal = re.compile('face=".*?"|FONT-FAMILY: 微软雅黑')
            item['contentHtml'] = re.sub(compal, '', contentHtml)

        item['typeId'] = type_polic(item)
        # 行业
        item['industry'] = ''
        #行业id
        item['industryId'] = ''
        # 附件名
        attachment_name = response.xpath(
            '//*[(contains(translate(@href, "PDF", "pdf"), ".pdf") or contains(translate(@href, "XLS", "xls"), ".xls") or contains(translate(@href, "DOC", "doc"), ".doc") or contains(translate(@href, "ZIP", "zip"), ".zip") or contains(translate(@href, "RAR", "rar"), ".rar") or contains(translate(@href, "WPS", "wps"), ".wps")) or contains(translate(@href, "XLSX", "xlsx"), ".xlsx") and not(contains(@href, "file://") or contains(@href, "c:\") or contains(@href, "c:\"))]/text() | .//*[contains(translate(@src, "MP4","mp4"), ".mp4") and not(contains(@src, "file://") or contains(@src,"c:\") or contains(@src, "C:\"))]/text()').getall()
        # 附件url
        attachment_url = response.xpath(
            '//*[(contains(translate(@href, "PDF", "pdf"), ".pdf") or contains(translate(@href, "XLS", "xls"), ".xls") or contains(translate(@href, "DOC", "doc"), ".doc") or contains(translate(@href, "ZIP", "zip"), ".zip") or contains(translate(@href, "RAR", "rar"), ".rar") or contains(translate(@href, "WPS", "wps"), ".wps")) or contains(translate(@href, "XLSX", "xlsx"), ".xlsx")  and not(contains(@href, "file://") or contains(@href, "c:\") or contains(@href, "c:\"))]/@href | .//*[contains(translate(@src, "MP4","mp4"), ".mp4") and not(contains(@src, "file://") or contains(@src,"c:\") or contains(@src, "C:\"))]/@src').getall()
        #整合name和url
        file_name = 'name'  # json 每一项中第一项的key
        file_url = 'url'  # json 每一项中第二项的key
        file_list = []
        for item1, item2 in zip(attachment_name, attachment_url):
            item2 = response.urljoin(item2)
            file_dic = {file_name: item1.strip(), file_url: item2.strip()}
            file_list.append(file_dic)
        item['attachments'] = file_list
        yield item

