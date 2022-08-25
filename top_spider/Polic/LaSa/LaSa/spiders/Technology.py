import copy
import re
import time

import scrapy
from lxml import etree

from .msBureau import *


class TachnologySpider(scrapy.Spider):
    name = 'Technology'
    allowed_domains = ['sti.xizang.gov.cn']
    start_urls = ['http://sti.xizang.gov.cn/xxgk/tzgg/index.html',
                  'http://sti.xizang.gov.cn/xxgk/Laws/index.html',
                  'http://sti.xizang.gov.cn/xxgk/gfxwj/index.html',
                  'http://sti.xizang.gov.cn/xxgk/zcjd/index.html']

    # http://sti.xizang.gov.cn/xxgk/tzgg/index.html # 公告公式 23
    # http://sti.xizang.gov.cn/xxgk/Laws/index.html # 法律法规 3
    # http://sti.xizang.gov.cn/xxgk/gfxwj/index.html# 规范性文件 2
    # http://sti.xizang.gov.cn/xxgk/zcjd/index.html # 政策解读 1

    # def start_requests(self):
    #     for p in range(24):
    #         p = f"_{p}" if p else ""
    #         url = f"http://sti.xizang.gov.cn/xxgk/tzgg/index{p}.html"
    #         yield scrapy.Request(url=url, callback=self.parse, dont_filter=True)

    def parse(self, response):
        item = {}

        list_url = response.xpath('//*[@class="gl-l"]//li/a/@href').getall()
        for href in list_url:
            item['url'] = response.urljoin(href)
            yield scrapy.Request(item['url'], callback=self.parse_info, meta={'item': copy.deepcopy(item)}
                                 , dont_filter=True)
        pass

    def parse_info(self, response):
        item = response.meta['item']

        item['title'] = response.xpath('//*[@class="xl-title"]/text()').get().strip()

        item['cityId'] = 1604

        item['classifyId'] = ''

        item['administrativeId'] = ''

        # 正文
        # 去除js和css节点
        html = etree.HTML(response.text)
        for elem in html.xpath('//style|//script'):
            elem.getparent().remove(elem)
        content = html.xpath('//*[@class="xl-articlecont xl-article"]//text()')
        sss = ''
        for i in content:
            sss = sss + i
        # 去除
        item['content'] = sss.strip()
        div_data = html.xpath('//*[@class="xl-articlecont xl-article"]')
        p_list = div_data[0].xpath('.//*')
        # 遍历所有的P标签，将里边的src,oldsrc属性拼接上前半部分
        for p in p_list:
            try:
                src_data = p.xpath('.//@src')[0]
                p.attrib['src'] = response.urljoin(src_data)
            except:
                pass
            try:
                src_data1 = p.xpath('.//@href')[0]
                p.attrib['href'] = response.urljoin(src_data1)
            except:
                pass
        # 将新的正标标签转成str保存
        contentHtml = etree.tostring(div_data[0], encoding='utf-8').decode()
        # 去除标签中的样式 如字体中的font样式
        compal = re.compile('style=".*?"')
        item['contentHtml'] = re.sub(compal, '', contentHtml)
        # 时间
        pub_date = response.xpath('//*[contains(text(),"来源：")]/preceding::span[1]/text()').get()
        timeArray = time.strptime(pub_date, '%Y年%m月%d日')
        timeStamp = int(time.mktime(timeArray)) * 1000
        item['publishTime'] = timeStamp
        # 新闻类型
        item['typeId'] = type_polic(item)
        # 来源
        item['sourceSite'] = '拉萨市科学技术厅'
        # 行业
        item['industry'] = ''
        # 行业id
        item['industryId'] = ''
        # 附件名
        attachment_name = re.findall(r'附件.：([^\.]+.[^\<]+)</a>', response.text)
        # 附件url
        attachment_url = re.findall(r'href="(.\/[^\.]+.[^\"]+)">附件', response.text)
        # 整合name和url
        file_name = 'name'  # json 每一项中第一项的key
        file_url = 'url'  # json 每一项中第二项的key
        file_list = []
        for item1, item2 in zip(attachment_name, attachment_url):
            item2 = response.urljoin(item2)
            file_dic = {file_name: item1.strip(), file_url: item2.strip()}
            file_list.append(file_dic)
        item['attachments'] = file_list

        #print(item['attachments'])

        yield item
