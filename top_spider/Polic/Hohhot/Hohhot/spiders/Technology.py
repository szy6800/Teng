# -*- coding: utf-8 -*-
import scrapy
import time
import re
from lxml import etree
import copy
from .msBureau import type_polic,index
import htmlmin
#  http://kjj.huhhot.gov.cn/tzgg/tzggList.shtml

class GovSpider(scrapy.Spider):
    name = 'Technology'
    allowed_domains = ['huhhot.gov.cn']
    start_urls = ['http://kjj.huhhot.gov.cn/tzgg_interface/article/notice_by_object.action?sslb=&startDate=1990-01-01&endDate=2999-01-01&content=&page={}'.format(i) for i in range(1,2)]

    def parse(self, response):
        # print(response.text)
        item = {}
        list_url = re.findall('/article/.*?shtml',response.text)
        #循环遍历
        for href in list_url:
            item['url'] = response.urljoin(href.strip())
            # print(item['url'])
            yield scrapy.Request(item['url'], callback=self.parse_info, meta={'item': copy.deepcopy(item)},
                                 dont_filter=True)

    def parse_info(self, response):
        item = response.meta['item']
        # 标题
        item['title'] = response.xpath('//*[@class="Wide-Content-title"]/text()').get().strip()
        # 城市id 467
        item['cityId'] = 467

        item['classifyId'] = ''
        # 大分类_id 人力
        item['administrativeId'] = ''
        # 正文
        # 去除js和css节点
        html = etree.HTML(response.text)
        for elem in html.xpath('//style|//script|//*[@id="xl_jd"]|//*[@class="xl-btn-box phone_none"]|//*[@id="qrcode"]'):
            elem.getparent().remove(elem)
        content = html.xpath('//*[@class="Wide-Content-text"]//text()')
        sss = ''
        for i in content:
            sss = sss + i
        # 去除
        item['content'] = sss.strip()
        div_data = html.xpath('//*[@class="Wide-Content-text"]')
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
        #contentHtml = htmlmin.minify(contentHtml)
        compal = re.compile('style=".*?"|http://swj.hefei.gov.cn/assets/images/files2/.*?gif|face=".*?"')
        contentHtml = re.sub(compal, '', contentHtml)
        try:
            tables = html.xpath('//*[@class="Wide-Content-text"]//table/@width')[0]
            item['contentHtml'] = re.sub(tables, '', contentHtml)
        except:
            item['contentHtml'] = re.sub(compal, '', contentHtml)

        pub_date = response.xpath("//*[contains(text(),'发布时间：')]").get()
        pub_date = re.findall('\d{4}-\d{2}-\d{2}',pub_date)[0]
        timeArray = time.strptime(pub_date, "%Y-%m-%d")
        timeStamp = int(time.mktime(timeArray)) * 1000
        item['publishTime'] = timeStamp

        # 新闻类型
        item['typeId'] = type_polic(item)
        # 来源
        item['sourceSite'] = '呼和浩特市科学技术局'
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
        item['att achments'] = file_list

        yield item
