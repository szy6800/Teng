# -*- coding: utf-8 -*-
import re
import scrapy
import copy
import time
from lxml import etree
from .Market_text import index, type_polic

class WjSpider(scrapy.Spider):
    name = 'Market'
    allowed_domains = ['amr.qingdao.gov.cn']

    def start_requests(self):
        for each in index():
            cate = each["cate"]
            pages = each["pages"]
            for p in range(pages):
                p = f"_{p + 1}" if p else ""
                url = f"http://amr.qingdao.gov.cn/{cate}{p}.html"
                # print(url)
                yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        item = {}
        list_url = response.xpath('//*[@class="category-list"]/li/a/@href').getall()
        titles = response.xpath('//*[@class="category-list"]/li/a/@title').getall()
        pub_times = response.xpath('//*[@class="category-list"]/li/a/following::span[1]').getall()

        for href,title,pub_time in zip(list_url,titles,pub_times):
            item['url'] = response.urljoin(href)
            item['title'] = title
            pub_date = re.findall(r'\d{4}-\d{2}-\d{2}',pub_time)[0]
            timeArray = time.strptime(pub_date, "%Y-%m-%d")
            timeStamp = int(time.mktime(timeArray)) * 1000
            # print(timeStamp,item['title'],item['url'])
            item['publishTime'] = timeStamp
            yield scrapy.Request(item['url'], callback=self.parse_info, meta={'item': copy.deepcopy(item)})

    def parse_info(self, response):
        item = response.meta['item']
        # 城市id
        item['cityId'] = 1211
        # 主题_id
        item['classifyId'] = ''
        # 大分类_id
        item['administrativeId'] = 1
        # 正文
        # 去除js和css节点
        html = etree.HTML(response.text)
        for elem in html.xpath('//style|//script'):
            elem.getparent().remove(elem)
        content = html.xpath('//*[@class="content"]//text()')
        sss = ''
        for i in content:
            sss = sss + i
        # 去除
        item['content'] = sss.strip()
        #带html标签
        div_data = html.xpath('//*[@class="content"]')
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
        item['contentHtml'] = re.sub(compal, '', contentHtml)
        # 新闻类型
        item['typeId'] = type_polic(item)
        # 大分类
        # 来源
        item['sourceSite'] = '青岛市市场监督管理局'
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



