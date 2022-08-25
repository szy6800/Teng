# -*- coding: utf-8 -*-
import scrapy
import time

from bs4 import BeautifulSoup
from lxml import etree
import copy
from .Tax_text import index
import re


class KuSpider(scrapy.Spider):
    name = 'Tax'
    allowed_domains = ['shanghai.chinatax.gov.cn']
    # start_urls = ['http://shanghai.chinatax.gov.cn/zcfw/zcjd/index_{}.html'.format(i) for i in range(20,30)]

    def start_requests(self):
        for each in index():
            cate = each["cate"]
            pages = each["pages"]
            for p in range(pages):
                p = f"_{p + 1}" if p else ""
                url = f"http://shanghai.chinatax.gov.cn/{cate}{p}.html"
                yield scrapy.Request(url=url, callback=self.parse)


    def parse(self, response):
        item = {}
        list_url = response.xpath('//*[@id="zcfglist"]/li/a/@href|//*[@class="infolist"]//li/a/@href').getall()
        # 循环遍历
        for href in list_url:
            item['url'] = response.urljoin(href)
            yield scrapy.Request(item['url'], callback=self.parse_info, meta={'item': copy.deepcopy(item)})

    def parse_info(self, response):
        item = response.meta['item']
        # 标题
        item['title'] = response.xpath("//*[@name='ArticleTitle']/@content").get().strip()
        # 城市
        item['city'] = '上海市'
        # 城市id
        item['cityId'] = 1433
        # 主题
        item['subject'] = ''
        # 主题_id
        item['classifyId'] = 2
        # 大分类
        item['big_type'] = '税务'
        # 大分类_id
        item['administrativeId'] = 2
        # 正文
        # 去除js和css节点
        html = etree.HTML(response.text)
        for elem in html.xpath('//style|//script'):
            elem.getparent().remove(elem)
        content = html.xpath('//*[@id="ivs_content"]//text()')
        sss = ''
        for i in content:
            sss = sss + i
        item['content'] = sss.strip()

        div_data = html.xpath('//*[@id="ivs_content"]')
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
        item['contentHtml'] = etree.tostring(div_data[0], encoding='utf-8').decode()

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
        # 新闻类型
        if '解读' in item['title']:
            item['typeId'] = 3
        elif '通告' in item['title']:
            item['typeId'] = 2
        elif '公告' in item['title']:
            item['typeId'] = 2
        elif '通知' in item['title']:
            item['typeId'] = 1
        elif '服务' in item['title']:
            item['typeId'] = 4
        elif '指南' in item['title']:
            item['typeId'] = 4
        elif '？' in item['title']:
            item['typeId'] = 4
        elif '法' in item['title']:
            item['typeId'] = 5
        elif '条例' in item['title']:
            item['typeId'] = 5
        else:
            item['typeId'] = 1
        # 来源
        item['sourceSite'] = response.xpath("//*[@name='SiteName']/@content").get()
        # 行业
        item['industry'] = ''
        # 行业id
        item['industryId'] = ''
        # 附件名
        attachment_name = response.xpath(
            '//*[(contains(translate(@href, "PDF", "pdf"), ".pdf") or contains(translate(@href, "XLS", "xls"), ".xls") or contains(translate(@href, "DOC", "doc"), ".doc") or contains(translate(@href, "ZIP", "zip"), ".zip") or contains(translate(@href, "RAR", "rar"), ".rar") or contains(translate(@href, "WPS", "wps"), ".wps")) and not(contains(@href, "file://") or contains(@href, "c:\") or contains(@href, "c:\"))]/text() | .//*[contains(translate(@src, "MP4","mp4"), ".mp4") and not(contains(@src, "file://") or contains(@src,"c:\") or contains(@src, "C:\"))]/text()').getall()
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



