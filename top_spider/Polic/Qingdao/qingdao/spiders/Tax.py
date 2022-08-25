# -*- coding: utf-8 -*-
import scrapy
import re
import copy
import time
from lxml import etree
from .Tax_text import index, type_polic


class WjSpider(scrapy.Spider):
    name = 'Tax'
    allowed_domains = ['qingdao.chinatax.gov.cn']

    def start_requests(self):
        for each in index():
            cate = each["cate"]
            pages = each["pages"]
            for p in range(pages):
                p = f"_{p}" if p else ""
                url = f"http://qingdao.chinatax.gov.cn/{cate}{p}.html"
                # print(url)
                yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        item = {}
        list_url = response.xpath('//*[@class="pc_15_ul"]/li/a/@href|//*[@class="pc_normal_content_ul"]/li/a/@href|//*[@class="p_15_ul"]/li/a/@href').getall()
        titles = response.xpath('//*[@class="pc_15_ul"]/li/a/@title|//*[@class="pc_normal_content_ul"]/li/a/@title|//*[@class="p_15_ul"]/li/a/@title').getall()
        pub_times = response.xpath('//*[@class="pc_15_ul"]/li/a/following::span[1]/text()|//*[@class="pc_normal_content_ul"]/li/a/following::span[1]/text()|//*[@class="p_15_ul"]/li/a/following::span[1]/text()').getall()

        for href,title,pub_time in zip(list_url,titles,pub_times):
            item['url'] = response.urljoin(href).replace(" ",'')
            # print(item['url'])
            item['title'] =title
            timeArray = time.strptime(pub_time.strip(), "%Y-%m-%d")
            timeStamp = int(time.mktime(timeArray)) * 1000
            item['publishTime'] = timeStamp
            yield scrapy.Request(item['url'], callback=self.parse_info, meta={'item': copy.deepcopy(item)})
    # #
    def parse_info(self, response):
        item = response.meta['item']
        # 城市id
        item['cityId'] = 1211
        # 主题_id
        item['classifyId'] = 2
        # 大分类_id
        item['administrativeId'] = 2
        # 正文
        # 去除js和css节点
        html = etree.HTML(response.text)
        for elem in html.xpath('//style|//script'):
            elem.getparent().remove(elem)
        content = html.xpath('//*[@class="p_wzxqy_content"]//text()')
        sss = ''
        for i in content:
            sss = sss + i
        # 去除
        item['content'] = sss.strip()
        div_data = html.xpath('//*[@class="p_wzxqy_content"]')
        p_list = div_data[0].xpath('.//*')
        # 遍历所有p标签，将里边的src,oldsrc属性拼接上前半部分
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
        contentHtml = etree.tostring(div_data[0], encoding='utf-8').decode().replace('附件:','')
        compal = re.compile('style=".*?"')
        item['contentHtml'] = re.sub(compal, '', contentHtml)
        # 新闻类型
        item['typeId'] = type_polic(item)
        # 来源
        item['sourceSite'] = '青岛市税务总局'
        # 行业
        item['industry'] = ''
        # 行业id
        item['industryId'] = ''
        # 附件名
        att_list = response.xpath(
            '//*[(contains(translate(@href, "PDF", "pdf"), ".pdf") or contains(translate(@href, "XLS", "xls"), ".xls") or contains(translate(@href, "DOC", "doc"), ".doc") or contains(translate(@href, "ZIP", "zip"), ".zip") or contains(translate(@href, "RAR", "rar"), ".rar") or contains(translate(@href, "WPS", "wps"), ".wps")) and not(contains(@href, "file://") or contains(@href, "c:\") or contains(@href, "c:\"))]/text() | .//*[contains(translate(@src, "MP4","mp4"), ".mp4") and not(contains(@src, "file://") or contains(@src,"c:\") or contains(@src, "C:\"))]/text()').getall()
        if att_list == []:
            # 附件名
            atts = response.xpath('//*[@id="xgfj"]//script//text()').getall()[0]
            attachment_url = re.findall("var sUrl = '(.*)';", atts)
            attachment_name = re.findall("var sDesc = '(.*)';", atts)
            if attachment_url == ['']:
                item['attachments'] = []
                yield item
            else:
                # 附件url
                # # 整合name和url
                file_name = 'name'  # json 每一项中第一项的keyxlsx
                file_url = 'url'  # json 每一项中第二项的key
                file_list = []
                for item1, item2 in zip(attachment_name, attachment_url):
                    item1 = item1.split(',')
                    item2 = item2.split(',')
                    for item1, item2 in zip(item1, item2):
                        item2 = response.urljoin(item2).replace(response.url, '')
                        file_dic = {file_name: item1.strip(), file_url: item2.strip()}
                        file_list.append(file_dic)
                    item['attachments'] = file_list
                    yield item
        else:
            attachment_name = response.xpath(
                '//*[@class="p_wzxqy_content"]//*[(contains(translate(@href, "PDF", "pdf"), ".pdf") or contains(translate(@href, "XLS", "xls"), ".xls") or contains(translate(@href, "DOC", "doc"), ".doc") or contains(translate(@href, "ZIP", "zip"), ".zip") or contains(translate(@href, "RAR", "rar"), ".rar") or contains(translate(@href, "WPS", "wps"), ".wps")) and not(contains(@href, "file://") or contains(@href, "c:\") or contains(@href, "c:\"))]/text() | .//*[contains(translate(@src, "MP4","mp4"), ".mp4") and not(contains(@src, "file://") or contains(@src,"c:\") or contains(@src, "C:\"))]/text()').getall()
            # 附件url
            attachment_url = response.xpath(
                '//*[@class="p_wzxqy_content"]//*[(contains(translate(@href, "PDF", "pdf"), ".pdf") or contains(translate(@href, "XLS", "xls"), ".xls") or contains(translate(@href, "DOC", "doc"), ".doc") or contains(translate(@href, "ZIP", "zip"), ".zip") or contains(translate(@href, "RAR", "rar"), ".rar") or contains(translate(@href, "WPS", "wps"), ".wps")) and not(contains(@href, "file://") or contains(@href, "c:\") or contains(@href, "c:\"))]/@href | .//*[contains(translate(@src, "MP4","mp4"), ".mp4") and not(contains(@src, "file://") or contains(@src,"c:\") or contains(@src, "C:\"))]/@src').getall()
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

