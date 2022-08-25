import copy
import re
import time

from lxml import etree

import scrapy

from .msBureau import *

#教育局
class EducationSpider(scrapy.Spider):
    name = 'Education'
    allowed_domains = ['jyj.lasa.gov.cn']
    start_urls = ['http://jyj.lasa.gov.cn/jiaoyuju/tggs/common_list.shtml',
                  'http://jyj.lasa.gov.cn/jiaoyuju/zcjd/common_list.shtml',
                  'http://jyj.lasa.gov.cn/jiaoyuju/gfxwj/common_list.shtml']

    # http://jyj.lasa.gov.cn/jiaoyuju/tggs/common_list.shtml # 公告公式 3
    # http://jyj.lasa.gov.cn/jiaoyuju/zcjd/common_list.shtml # 政策解读 1
    # http://jyj.lasa.gov.cn/jiaoyuju/gfxwj/common_list.shtml # 规范性文件 1

    # def start_requests(self):
    #     for p in range(1):
    #         p = f"_{p}" if p else ""
    #         url = f"http://jyj.lasa.gov.cn/jiaoyuju/gfxwj/common_list{p}.shtml"
    #         yield scrapy.Request(url=url, callback=self.parse, dont_filter=True)

    def parse(self, response):
        item = {}

        list_url = response.xpath('//*[@id="list-data"]//ul/li/a/@href').getall()
        for href in list_url:
            item['url'] = response.urljoin(href)
            yield scrapy.Request(item['url'], callback=self.parse_info, meta={'item': copy.deepcopy(item)}
                                 , dont_filter=True)

    def parse_info(self, response):
        item = response.meta['item']

        item['title'] = response.xpath('//*[@class="detail"]//h1/text()').get().strip()

        item['cityId'] = 1604

        item['classifyId'] = ''

        item['administrativeId'] = ''

        # 正文
        # 去除js和css节点
        html = etree.HTML(response.text)
        for elem in html.xpath('//style|//script'):
            elem.getparent().remove(elem)
        content = html.xpath("//*[@id='NewsContent']//text()")
        sss = ''
        for i in content:
            sss = sss + i
        # 去除
        item['content'] = sss.strip()
        # html标签
        div_data = html.xpath("//*[@id='NewsContent']")
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
        pub_date = response.xpath("//*[@name='PubDate']/@content").get()
        timeArray = time.strptime(pub_date, '%Y-%m-%d %H:%M:%S')
        timeStamp = int(time.mktime(timeArray)) * 1000
        item['publishTime'] = timeStamp
        # 新闻类型
        item['typeId'] = type_polic(item)
        # 来源
        item['sourceSite'] = '拉萨市市场监督管理局'
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

        print(item['attachments'])
        yield item
