# -*- coding: utf-8 -*-
import scrapy
import time
import re
from lxml import etree
import copy
from .Market_text import index


class Pro1zhinanSpider(scrapy.Spider):
    name = 'Market'
    allowed_domains = ['scjgj.sh.gov.cn']

    def start_requests(self):
        for each in index():
            cate = each["cate"]
            pages = each["pages"]
            for p in range(pages):
                p = f"_{p + 1}" if p else ""
                url = f"http://scjgj.sh.gov.cn/{cate}/index{p}.html"
                yield scrapy.Request(url=url, callback=self.parse)

    # start_urls = ['http://scjgj.sh.gov.cn/056/index_{}.html'.format(i) for i in range(2,38)]

    def parse(self, response):
        item = {}
        list_url = response.xpath('//*[@class="overflow"]/a/@href').getall()
        # 发布时间
        pub_dates = response.xpath('//*[@class="overflow"]/a/@href/following::td[1]/text()').getall()
        # 循环遍历
        for href, pub_date in zip(list_url, pub_dates):
            item['url'] = response.urljoin(href)
            timeArray = time.strptime(pub_date, "%Y-%m-%d")
            timeStamp = int(time.mktime(timeArray)) * 1000
            item['publishTime'] = timeStamp
            yield scrapy.Request(item['url'], callback=self.parse_info, meta={'item': copy.deepcopy(item)})

    def parse_info(self, response):
        item = response.meta['item']
        # 标题
        item['title'] = response.xpath("//*[@id='ivs_title']/text()").get().strip()
        # 城市名称
        item['city'] = '上海市'
        # 城市id
        item['cityId'] = 1433
        # 主题
        item['subject'] = ''
        # 主题_id
        item['classifyId'] = ''
        # 大分类
        item['big_type'] = '工商'
        # 大分类_id
        item['administrativeId'] = 1
        # 正文
        # 去除js和css节点
        html = etree.HTML(response.text)
        for elem in html.xpath('//style|//script'):
            elem.getparent().remove(elem)
        content = html.xpath('//*[@id="ivs_content"]//text()')
        sss = ''
        for i in content:
            sss = sss + i
        # 去除
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
        contentHtml = etree.tostring(div_data[0], encoding='utf-8').decode()
        compal = re.compile('style=".*?"')
        item['contentHtml'] = re.sub(compal, '', contentHtml)
        # 新闻类型
        if '解读' in item['title']:
            item['typeId'] = 3
        elif '通告' in item['title']:
            item['typeId'] = 2
        elif '公告' in item['title']:
            item['typeId'] = 2
        elif '通知' in item['title']:
            item['typeId'] = 1
        elif '申报' in item['title']:
            item['typeId'] = 4
        elif '建议' in item['title']:
            item['typeId'] = 4
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
        item['sourceSite'] = '上海市场监管局'
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

