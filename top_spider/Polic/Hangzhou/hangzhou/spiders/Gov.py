# -*- coding: utf-8 -*-
import scrapy
import time
import re
from lxml import etree
import copy
from .wj_text import type_polic,index
import json,jsonpath

#   http://kj.hangzhou.gov.cn/col/col1693961/index.html
class WjSpider(scrapy.Spider):
    name = 'Gov'
    allowed_domains = ['hangzhou.gov.cn']

    def start_requests(self):
        # 构建url
        for i in range(1,2):
                url = 'http://www.hangzhou.gov.cn/module/xxgk/search.jsp?standardXxgk=0&isAllList=1&texttype=&fbtime=&vc_all=&vc_filenumber=&vc_title=&vc_number=&currpage={}&sortfield=,createdatetime:0,orderid:0'.format(i)
                # 构建post请求参数
                data = {
                    'infotypeId': 'F01000020101',
                    'jdid': '149',
                    'area':'',
                    'divid': 'div1510978',
                    'vc_title':'',
                    'vc_number':'',
                    'sortfield': 'createdatetime: 0, orderid: 0',
                    'vc_filenumber':'',
                    'vc_all':'',
                    'texttype':'',
                    'fbtime':'',
                    'standardXxgk': '0',
                    'isAllList': '1',
                    'currpage': '{}'.format(i),
                }
            # 发送post请求
                yield scrapy.FormRequest(url=url, formdata=data, callback=self.parse)

    # 解析详情url
    def parse(self, response):
        item = {}
        # print(response.text)
        list_url = re.findall('http://www.hangzhou.gov.cn/art/.*?html', response.text)
        for href in list_url:
            item['url'] = response.urljoin(href)
            # print(item['url'])
            yield scrapy.Request(item['url'], callback=self.parse_info, meta={'item': copy.deepcopy(item)})

    # 解析内容
    def parse_info(self, response):
        item = response.meta['item']

        item['title'] = response.xpath("//*[@name='ArticleTitle']/@content").get()
        # 城市id
        item['cityId'] = 2803
        # 主题_id
        item['classifyId'] = 10
        # 大分类_id
        item['administrativeId'] = ''
        # 正文
        # 去除js和css节点
        html = etree.HTML(response.text)
        for elem in html.xpath('//style|//script'):
            elem.getparent().remove(elem)
        content = html.xpath('//*[@id="zoom"]//text()|//*[@class="article"]//text()')
        sss = ''
        for i in content:
            sss = sss + i
        # 去除
        item['content'] = sss.strip()
        # print(item['content'])

        div_data = html.xpath('//*[@id="zoom"]|//*[@class="article"]')
        p_list = div_data[0].xpath('.//*' )
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
            tables = html.xpath('//*[@class="article"]//table/@width')[0]
            item['contentHtml'] = re.sub(tables, '', contentHtml)
        except:
            item['contentHtml'] = re.sub(compal, '', contentHtml)
        # 新闻类型来源
        item['typeId'] = type_polic(item)
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

        item['sourceSite'] = '杭州市人民政府'
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
