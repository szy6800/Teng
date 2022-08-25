import copy
import re
import time

from lxml import etree

import scrapy

#税务局--通知公告
from .msBureau import *


class TaxNoticeSpider(scrapy.Spider):
    name = 'Tax_Notice'
    allowed_domains = ['xizang.chinatax.gov.cn']
    # https://xizang.chinatax.gov.cn/module/web/jpage/dataproxy.jsp?startrecord=301&endrecord=360&perpage=20 # 通知公告 365 1 60

    def start_requests(self):
        # 构建url
        for l1, l2 in zip(range(1, 45, 60), range(46, 90, 60)):  # 365
            url = 'https://xizang.chinatax.gov.cn/module/web/jpage/dataproxy.jsp?startrecord={}&endrecord={}&perpage=15'.format(
                l1, l2)
            # 构建post请求参数
            data = {
                "col": "1",
                "appid": "1",
                "webid": "1",
                "path": "/",
                "columnid": "3977",
                "sourceContentType": "1",
                "unitid": "27343",
                "webname": "国家税务总局西藏自治区税务局",
                "permissiontype": "0",
            }
            yield scrapy.FormRequest(url=url, formdata=data, callback=self.parse)

    def parse(self, response):
        item = {}
        res = etree.HTML(response.text)
        print(res)
        list_url = res.xpath('//recordset//record//a/@href')
        for href in list_url:
            item['url'] = response.urljoin(href)
            yield scrapy.Request(item['url'], callback=self.parse_info, meta={'item': copy.deepcopy(item)})
        pass

    def parse_info(self, response):

        item = response.meta['item']

        item['title'] = response.xpath('//*[@id="title"]/text()').get().strip()

        item['cityId'] = 1604

        item['classifyId'] = ''

        item['administrativeId'] = ''
        # 正文
        # 去除js和css节点
        html = etree.HTML(response.text)
        for elem in html.xpath('//style|//script'):
            elem.getparent().remove(elem)
        content = html.xpath('//*[@id="zoom"]//text()')
        sss = ''
        for i in content:
            sss = sss + i
        # 去除
        item['content'] = sss.strip()
        # print(item['content'])
        # 解析带html的详情
        div_data = html.xpath('//*[@id="zoom"]')
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
        # 将新的正标标签转成str保存
        contentHtml = etree.tostring(div_data[0], encoding='utf-8').decode()
        # 去除标签中的样式 如字体中的font样式
        compal = re.compile('style=".*?"')
        item['contentHtml'] = re.sub(compal, '', contentHtml)
        # 时间
        pub_date = response.xpath("//*[@name='PubDate']/@content").get()
        try:
            timeArray = time.strptime(pub_date, "%Y-%m-%d %H:%M")
        except:
            timeArray = time.strptime(pub_date, "%Y-%m-%d")
        timeStamp = int(time.mktime(timeArray)) * 1000
        item['publishTime'] = timeStamp
        # 新闻类型
        item['typeId'] = type_polic(item)
        item['sourceSite'] = '拉萨市税务局'
        # 行业
        item['industry'] = ''
        # 行业id
        item['industryId'] = ''
        # 附件名
        attachment_name = method_name(response)
        # 附件url
        attachment_url = methodNameUrl(response)
        # 整合name和url
        file_name = 'name'  # json 每一项中第一项的key
        file_url = 'url'  # json 每一项中第二项的key
        file_list = []
        for item1, item2 in zip(attachment_name, attachment_url):
            item2 = response.urljoin(item2)
            file_dic = {file_name: item1.strip(), file_url: item2.strip()}
            file_list.append(file_dic)
        item['attachments'] = file_list
        print(item)
        yield item
