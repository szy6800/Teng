# -*- coding: utf-8 -*-
import scrapy
import copy
import time,re
from lxml import etree
from .wj_text import *

#  通知公告 https://henan.chinatax.gov.cn/zhengzhou/tzgg/tzgg/e35d8ca2-1.html

class WjSpider(scrapy.Spider):
    name = 'Tax'
    allowed_domains = ['henan.chinatax.gov.cn']
    start_urls = ['https://henan.chinatax.gov.cn/eportal/ui?pageId=65a6d96439804ccd91723da8d1d037f4&currentPage={}&moduleId=e35d8ca2d03b41a1bec879b95e170529&staticRequest=yes'.format(i) for i in range(1,2)] # 65


    def parse(self, response):
        item = {}
        # # 反序列化
        list_url = response.xpath('//*[@class="listCon"]//li/a/@href').getall()
        pub_dates = response.xpath('//*[@class="listCon"]//li/a/following::span[1]/text()').getall()
        titles = response.xpath('//*[@class="listCon"]//li/a/@title').getall()
        # 循环遍历
        for href, pub_date, title in zip(list_url, pub_dates, titles):
            item['url'] = response.urljoin(href)
            timeArray = time.strptime(pub_date.strip(), "%Y-%m-%d")
            timeStamp = int(time.mktime(timeArray)) * 1000
            item['publishTime'] = timeStamp
            item['title'] = title
            # print(item['url'],item['title'],item['publishTime'])
            yield scrapy.Request(item['url'], callback=self.parse_info, meta={'item': copy.deepcopy(item)})

    def parse_info(self, response):
        item = response.meta['item']
        # 城市id
        item['cityId'] = 153

        item['classifyId'] = 2
        # 大分类_id
        item['administrativeId'] = 2
        # 正文
        # 去除js和css节点和多余的文字
        html = etree.HTML(response.text)
        for elem in html.xpath('//style|//script|//*[@id="articleEwm"]'):
            elem.getparent().remove(elem)
        content = html.xpath('//*[@id="mainText"]//text()')
        sss = ''
        for i in content:
            sss = sss + i
        # 去除
        item['content'] = sss.strip()
        div_data = html.xpath('//*[@id="mainText"]')
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
        compal = re.compile(
            'style=".*?"|face=".*?"')
        contentHtml = re.sub(compal, '', contentHtml)
        try:
            tables = html.xpath('//*[@id="mainText"]//table/@width')[0]
            item['contentHtml'] = re.sub(tables, '', contentHtml)
        except:
            item['contentHtml'] = re.sub(compal, '', contentHtml)

        # 新闻类型
        item['typeId'] = type_polic(item)
        # 来源
        item['sourceSite'] = response.xpath('//*[@name="SiteName"]/@content').get()
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

