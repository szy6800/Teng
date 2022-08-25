# -*- coding: utf-8 -*-
import scrapy
import time
import re
from lxml import etree
import copy
from .wj_text import type_polic,index
import json,jsonpath

#  杭州市商务局 http://sww.hangzhou.gov.cn/col/col1229460831/index.html?uid=4754249&pageNum=31


class WjSpider(scrapy.Spider):
    name = 'Commerce'
    allowed_domains = ['hangzhou.gov.cn']

    def start_requests(self):
        # 构建url
        for l1, l2 in zip(range(1, 60, 60), range(61, 120, 60)):
            url = 'http://sww.hangzhou.gov.cn/module/jpage/dataproxy.jsp?startrecord={}&endrecord={}&perpage=20'.format(
                l1, l2)
            # 构建post请求参数
            data = {
                'col': '1',
                'appid': '1',
                'webid': '3113',
                'path': '/',
                'columnid': '1229460831',
                'sourceContentType': '1',
                'unitid': '4754249',
                'webname': '杭州市商务局 杭州市粮食和物资储备局',
                'permissiontype': '0'
            }
            # 发送post请求
            yield scrapy.FormRequest(url=url, formdata=data, callback=self.parse)

    # 解析详情url
    def parse(self, response):

        item = {}
        from lxml import etree
        res = etree.HTML(response.text)
        list_url = res.xpath('//recordset//record//a/@href')

        for href in list_url:
            item['url'] = response.urljoin(href)
            # print(item['url'])
            yield scrapy.Request(item['url'], callback=self.parse_info, meta={'item': copy.deepcopy(item)})

    # 解析内容
    def parse_info(self, response):
        item = response.meta['item']

        item['title'] = response.xpath("//*[@name='ArticleTitle']/@content").get()
        # 城市id2803
        item['cityId'] = 2803
        # 主题_id
        item['classifyId'] = 2
        # 大分类_id
        item['administrativeId'] = 2
        # 正文
        # 去除js和css节点
        html = etree.HTML(response.text)
        for elem in html.xpath('//style|//script'):
            elem.getparent().remove(elem)
        content = html.xpath('//*[@id="zoom"]//text()|//*[@class="info-cont"]//text()')
        sss = ''
        for i in content:
            sss = sss + i
        # 去除
        item['content'] = sss.strip()
        # print(item['content'])

        div_data = html.xpath('//*[@id="zoom"]|//*[@class="info-cont"]')
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
        compal = re.compile('style=".*?"|http://zhejiang.chinatax.gov.cn/module/jslib/icons/.*?png')
        contentHtml = re.sub(compal, '', contentHtml)
        try:
            tables = html.xpath('//*[@id="zoom"]//table/@width')[0]
            item['contentHtml'] = re.sub(tables, '', contentHtml)
        except:
            item['contentHtml'] = re.sub(compal, '', contentHtml)
        # 新闻类型
        item['typeId'] = type_polic(item)
        # 来源
        try:
            pub_date = response.xpath("//*[@name='PubDate']/@content | //*[@http-equiv='PubDate']/@content").get()
            timeArray = time.strptime(pub_date, "%Y-%m-%d %H:%M")
            timeStamp = int(time.mktime(timeArray)) * 1000
            item['publishTime'] = timeStamp
        except:
            pub_date = response.xpath("//*[@name='PubDate']/@content | //*[@http-equiv='PubDate']/@content").get()
            timeArray = time.strptime(pub_date, "%Y-%m-%d")
            timeStamp = int(time.mktime(timeArray)) * 1000
            item['publishTime'] = timeStamp

        item['sourceSite'] = '杭州市商务局'
        # 行业
        item['industry'] = ''
        # 行业id
        item['industryId'] = ''
        # 附件名
        attachment_name = response.xpath(
            '//*[(contains(translate(@href, "PDF", "pdf"), ".pdf") or contains(translate(@href, "XLS", "xls"), ".xls") or contains(translate(@href, "DOC", "doc"), ".doc") or contains(translate(@href, "ZIP", "zip"), ".zip") or contains(translate(@href, "RAR", "rar"), ".rar") or contains(translate(@href, "WPS", "wps"), ".wps")) and not(contains(@href, "file://") or contains(@href, "c:\") or contains(@href, "c:\"))]//text() | .//*[contains(translate(@src, "MP4","mp4"), ".mp4") and not(contains(@src, "file://") or contains(@src,"c:\") or contains(@src, "C:\"))]//text()').getall()
        # 附件url
        attachment_url = response.xpath(
            '//*[(contains(translate(@href, "PDF", "pdf"), ".pdf") or contains(translate(@href, "XLS", "xls"), ".xls") or contains(translate(@href, "DOC", "doc"), ".doc") or contains(translate(@href, "ZIP", "zip"), ".zip") or contains(translate(@href, "RAR", "rar"), ".rar") or contains(translate(@href, "WPS", "wps"), ".wps")) and not(contains(@href, "file://") or contains(@href, "c:\") or contains(@href, "c:\"))]/@href | .//*[contains(translate(@src, "MP4","mp4"), ".mp4") and not(contains(@src, "file://") or contains(@src,"c:\") or contains(@src, "C:\"))]/@src').getall()
        # 整合name和url
        file_name = 'name'  # json 每一项中第一项的key
        file_url = 'url'  # json 每一项中第二项的key
        file_list = []
        for item1, item2 in zip(attachment_name, attachment_url):
            item2 = response.urljoin(item2)
            file_dic = {file_name: item1, file_url: item2}
            file_list.append(file_dic)
        item['attachments'] = file_list

        yield item
