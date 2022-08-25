# -*- coding: utf-8 -*-
import scrapy
import copy
import time
from lxml import etree
from .wj_text import type_polic
import re

# TODO 通知公告
class Wj1Spider(scrapy.Spider):
    name = 'Market'
    allowed_domains = ['scjg.hangzhou.gov.cn']
    # start_urls = ['http://scjg.hangzhou.gov.cn/']

    def start_requests(self):
        # 构建url
        for l1, l2 in zip(range(1, 30, 30), range(30, 60, 30)):
        # for l1, l2 in zip(range(1, 400, 30), range(400, 1100, 30)):
            url = 'http://scjg.hangzhou.gov.cn/module/jpage/dataproxy.jsp?startrecord={}&endrecord={}&perpage=10'.format(
                l1, l2)
            # 构建post请求参数
            data = {
                'col': '1',
                'appid': '1',
                'webid': '3246',
                'path': '/',
                'columnid': '1693484',
                'sourceContentType': '1',
                'unitid': '5100070',
                'webname': '杭州市市场监督管理局',
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
        titles = res.xpath('//recordset//record//a/@title')
        pub_dates = res.xpath('//recordset//record//a/following::span[1]/text()')

        for href, title, pub_date in zip(list_url, titles, pub_dates):
            item['url'] = response.urljoin(href)
            item['title'] = title.strip()
            timeArray = time.strptime(pub_date, "%Y-%m-%d")
            timeStamp = int(time.mktime(timeArray)) * 1000
            item['publishTime'] = timeStamp
            # print(item['url'],item['title'],item['publishTime'])
            yield scrapy.Request(item['url'], callback=self.parse_info, meta={'item': copy.deepcopy(item)})

        # 解析内容

    def parse_info(self, response):
        item = response.meta['item']
        # 城市id
        item['cityId'] = 2803
        # 主题_id
        item['classifyId'] = ''
        # 大分类_id
        item['administrativeId'] = 1
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
        # 将新的正文标签转成str保存
        contentHtml = etree.tostring(div_data[0], encoding='utf-8').decode().replace('附件：', '').replace('&#13;', '')
        compal = re.compile('style=".*?"|http://scjg.hangzhou.gov.cn/module/jslib/icons/.*?png')
        contentHtml = re.sub(compal, '', contentHtml)
        try:
            tables = html.xpath('//*[@id="zoom"]//table/@width')[0]
            item['contentHtml'] = re.sub(tables, '', contentHtml)
        except:
            item['contentHtml'] = re.sub(compal, '', contentHtml)
        # 新闻类型
        item['typeId'] = type_polic(item)
        # 来源
        item['sourceSite'] = response.xpath('//*[@name="subsite"]/@content').get()
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
            file_dic = {file_name: item1.strip(), file_url: item2.strip()}
            file_list.append(file_dic)
        item['attachments'] = file_list

        yield item