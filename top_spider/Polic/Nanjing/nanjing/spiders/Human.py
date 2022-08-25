# -*- coding: utf-8 -*-
import json

import scrapy
import time
import re
from lxml import etree
import copy,jsonpath
from .wj_text import type_polic,index

class WjSpider(scrapy.Spider):
    name = 'Human'
    allowed_domains = ['rsj.nanjing.gov.cn/']
    # start_urls = ['http://rsj.nanjing.gov.cn/igs/front/search/publish/data/list.html?&index=wzqsearch-v20190124&type=infomation&siteId=57&pageSize=20&orderProperty=DOCRELTIME&pageIndex=3&orderDirection=desc&filter%5BSITEID%5D=57&filter%5BCHANNELID%5D=&filter%5BGROUPCAT%5D=228&pageNumber={}'.format(i) for i in range(60,83)]
    # start_urls = ['http://rsj.nanjing.gov.cn/igs/front/search/publish/data/list.html?&index=wzqsearch-v20190124&type=infomation&siteId=57&pageSize=20&orderProperty=DOCRELTIME&pageIndex=3&orderDirection=desc&filter%5BSITEID%5D=57&filter%5BCHANNELID%5D=&filter%5BGROUPCAT%5D=224&pageNumber={}'.format(i) for i in range(1,27)]
    start_urls = ['http://rsj.nanjing.gov.cn/igs/front/search/publish/data/list.html?&index=wzqsearch-v20190124&type=infomation&siteId=57&pageSize=20&orderProperty=DOCRELTIME&pageIndex=3&orderDirection=desc&filter%5BSITEID%5D=57&filter%5BCHANNELID%5D=&filter%5BGROUPCAT%5D=224&pageNumber=1','http://rsj.nanjing.gov.cn/igs/front/search/publish/data/list.html?&index=wzqsearch-v20190124&type=infomation&siteId=57&pageSize=20&orderProperty=DOCRELTIME&pageIndex=3&orderDirection=desc&filter%5BSITEID%5D=57&filter%5BCHANNELID%5D=&filter%5BGROUPCAT%5D=224&pageNumber=1']

    # def start_requests(self):
    #     for each in index():
    #         cate = each["cate"]
    #         pages = each["pages"]
    #         for p in range(pages):
    #             p = f"_" if p else ""
    #             url = f"http://rsj.nanjing.gov.cn/{cate}{p}.html"
    #             yield scrapy.Request(url=url, callback=self.parse, dont_filter=True)

    def parse(self, response):
        # print(response.text)
        item = {}
        text = json.loads(response.text)
        list_url = jsonpath.jsonpath(text, '$..DOCPUBURL')
        # list_url = response.xpath("//*[@id='result']/li//a/@href").getall()
        # 循环遍历
        for href in list_url:
            # print(response.urljoin(href))
            item['url'] = response.urljoin(href.strip())
            yield scrapy.Request(item['url'], callback=self.parse_info, meta={'item': copy.deepcopy(item)},
                                 dont_filter=True)

    def parse_info(self, response):
        item = response.meta['item']
        # 标题
        item['title'] = response.xpath("//title/text()").get().strip()
        # 城市id 2293
        item['cityId'] = 2293

        item['classifyId'] = ''
        # 大分类_id 人力
        item['administrativeId'] = 3
        # 正文
        # 去除js和css节点
        html = etree.HTML(response.text)
        for elem in html.xpath('//style|//script|//*[@id="div_div"]|//*[@class="print"]|//*[@id="Canvas"]'):
            elem.getparent().remove(elem)
        content = html.xpath("//*[@class='con']//text()")
        sss = ''
        for i in content:
            sss = sss + i
        # 去除
        item['content'] = sss.strip()
        div_data = html.xpath("//*[@class='con']")
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
        contentHtml = etree.tostring(div_data[0], encoding='utf-8').decode().replace('附件：', '')
        compal = re.compile('style=".*?"|http://amr.ah.gov.cn/assets/images/files2/.*?gif|face=".*?"')
        contentHtml = re.sub(compal, '', contentHtml)
        try:
            tables = html.xpath('//*[@class="con"]//table/@width')[0]
            item['contentHtml'] = re.sub(tables, '', contentHtml)
        except:
            item['contentHtml'] = re.sub(compal, '', contentHtml)
        try:
            pub_date = response.xpath("//*[contains(text(),'生成日期：')]/following::td[1]/text()").get().strip()
            timeArray = time.strptime(pub_date, "%Y-%m-%d")
            timeStamp = int(time.mktime(timeArray)) * 1000
            item['publishTime'] = timeStamp
        except:
            pub_date = response.xpath("//*[contains(text(),'生成日期：')]/following::td[1]/text()").get().strip()
            timeArray = time.strptime(pub_date, "%Y-%m-%d")
            timeStamp = int(time.mktime(timeArray)) * 1000
            item['publishTime'] = timeStamp
        # 新闻类型
        item['typeId'] = type_polic(item)
        # 来源
        item['sourceSite'] = '南京市人力资源和社会保障局'
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
