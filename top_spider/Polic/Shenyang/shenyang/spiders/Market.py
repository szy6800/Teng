# -*- coding: utf-8 -*-
import scrapy
import time
import re
from lxml import etree
import copy
from .wj_text import type_polic,index

class WjSpider(scrapy.Spider):
    name = 'Market'
    allowed_domains = ['scj.shenyang.gov.cn']
    # start_urls = ['http://scj.shenyang.gov.cn/scjdglj/zwgkzdgz/zcyjd/tzgg/glist{}.html'.format(i) for i in range(150,200)] #200

    #
    def start_requests(self):
        for each in index():
            cate = each["cate"]
            pages = each["pages"]
            for p in range(pages):
                p = f"{p}" if p else ""
                url = f"http://scj.shenyang.gov.cn/{cate}{p}.html"
                yield scrapy.Request(url=url, callback=self.parse, dont_filter=True)

    def parse(self, response):
        item = {}
        # # 反序列化
        list_url = response.xpath('//*[@class="xxgk_rul"]/li/a/@href|//*[@class="list"]/li/a/@href').getall()
        titles = response.xpath('//*[@class="xxgk_rul"]/li/a/text()|//*[@class="list"]/li/a/text()').getall()
        times = response.xpath('//*[@class="xxgk_rul"]/li/a/following::span[1]/text()|//*[@class="list"]/li/a/following::div[1]//text()').getall()
        # 循环遍历
        for href, title, pub_date in zip(list_url,titles,times):
            timeArray = time.strptime(pub_date, "%Y-%m-%d")
            timeStamp = int(time.mktime(timeArray)) * 1000
            item['publishTime'] = timeStamp
            item['url'] = response.urljoin(href.strip())
            item['title'] = title
            # print(href, title, pub_date)
            yield scrapy.Request(item['url'], callback=self.parse_info, meta={'item': copy.deepcopy(item)})

    def parse_info(self, response):
        item = response.meta['item']
        # 标题
        # item['title'] = response.xpath("//*[@name=' ArticleTitle ']/@content").get()
        # 城市id
        item['cityId'] = 1117

        item['classifyId'] = ''
        # 大分类_id
        item['administrativeId'] = 1
        # 正文
        # 去除js和css节点
        html = etree.HTML(response.text)
        for elem in html.xpath('//style|//script|//*[@id="qrcode"]'):
            elem.getparent().remove(elem)
        content = html.xpath('//*[@class="center"]//text()')
        sss = ''
        for i in content:
            sss = sss + i
        # 去除
        item['content'] = sss.strip()
        div_data = html.xpath('//*[@class="center"]')
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
        compal = re.compile('style=".*?"|face=".*?"|http://www.shenyang.gov.cn/saas/plugins/ueditor/dialogs/attachment/fileTypeImages/icon_.*?.gif|http://scj.shenyang.gov.cn/saas/plugins/ueditor/dialogs/attachment/fileTypeImages/icon_.*?gif')
        contentHtml = re.sub(compal, '', contentHtml)
        try:
            tables = html.xpath('//*[@class="center"]//table/@width')[0]
            item['contentHtml'] = re.sub(tables, '', contentHtml)
        except:
            item['contentHtml'] = re.sub(compal, '', contentHtml)
        # 新闻类型
        item['typeId'] = type_polic(item)
        # 来源
        item['sourceSite'] = '沈阳市市场监督管理局'
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
