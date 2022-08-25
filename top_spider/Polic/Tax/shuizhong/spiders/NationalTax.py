# -*- coding: utf-8 -*-
import scrapy
import json
import jsonpath
import copy
from lxml import etree
import time
from .NationalTax_ import index,type_polic,file_type
# TODO 税种分类


class TaxSpider(scrapy.Spider):
    name = 'NationalTax'
    allowed_domains = ['chinatax.gov.cn']

    def start_requests(self):
        for each in index():
            cate = each["cate"]
            pages = each["pages"]
            for p in range(pages):
                p = f"{p+1}" if p else ""
                url = f"http://www.chinatax.gov.cn/api/query?siteCode=bm29000fgk&tab=all&key=9A9C42392D397C5CA6C1BF07E2E0AA6F?timeOption=0&C6={cate}&page={p}&pageSize=10&keyPlace=1&sort=dateDesc&qt=*"
                # print(url)
                yield scrapy.Request(url=url, callback=self.parse,dont_filter=True)

    def parse(self, response):
        item = {}
        # # 反序列化
        text = json.loads(response.text)
        list_url = jsonpath.jsonpath(text, '$..url')
        # 循环遍历
        for href in list_url:
            # print(href)
            item['url'] = response.urljoin(href)
            yield scrapy.Request(item['url'], callback=self.parse_info, meta={'item': copy.deepcopy(item)})

    def parse_info(self, response):
        item = response.meta['item']
        # 标题
        item['title'] = response.xpath("//*[@name='ArticleTitle']/@content").get()
        # 城市
        item['city'] = ''
        # 城市id
        item['cityId'] = ''
        # 主题
        item['subject'] = ''
        # 主题_id
        classifyId = response.xpath("//*[@name='ColumnName']/@content").get()

        item['classifyId'] = type_polic(item,classifyId)
        # 大分类
        item['big_type'] = ''
        # 大分类_id
        item['administrativeId'] = ''
        # 正文
        # 去除js和css节点
        html = etree.HTML(response.text)
        for elem in html.xpath('//style|//script|//*[@class="jiuc"]|//h3'):
            elem.getparent().remove(elem)
        content = html.xpath('//*[@id="fontzoom"]//text()')
        sss = ''
        for i in content:
            sss = sss + i
        # 去除
        item['content'] = sss.strip()

        div_data = html.xpath('//*[@id="fontzoom"]')
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
            timeArray = time.strptime(pub_date, "%Y-%m-%d %H:%M:%S")
            #转时间戳
            timeStamp = int(time.mktime(timeArray)) * 1000
            item['publishTime'] = timeStamp
        except:
            pub_date = response.xpath("//*[@name='PubDate']/@content | //*[@http-equiv='PubDate']/@content").get()
            timeArray = time.strptime(pub_date, "%Y-%m-%d")
            timeStamp = int(time.mktime(timeArray)) * 1000
            item['publishTime'] = timeStamp
        # 新闻类型
        item['typeId'] = file_type(item)
        # 来源
        item['sourceSite'] = '国家税务总局'
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