import copy
import json
import re
import time

import jsonpath
import scrapy
from lxml import etree

from .msBureau import type_polic, method_name, methodNameUrl

#科学技术局
class TechnologySpider(scrapy.Spider):
    name = 'Technology'
    allowed_domains = ['kgxj.haikou.gov.cn']
    # start_urls = ['http://kgxj.haikou.gov.cn/quicksilver/public/plugin/getListPaneData.json?siteAreaId=402849d0609c93c40160a0d4db1b00e6&count=20&index={}'.format(20, i) for i in range(1,33),]# 公示公告
    #                http://kgxj.haikou.gov.cn/quicksilver/public/plugin/getListPaneData.json?siteAreaId=402849d060a0d6720160a0d706600000&count=20&index=2 #政策文件 3
    #                http://kgxj.haikou.gov.cn/quicksilver/public/plugin/getListPaneData.json?siteAreaId=402849d060a0d6720160a0d9c953000f&count=20&index=4 #解读回应 5
    start_urls = [
        'http://kgxj.haikou.gov.cn/quicksilver/public/plugin/getListPaneData.json?siteAreaId=402849d0609c93c40160a0d4db1b00e6&count=20&index=1',
        'http://kgxj.haikou.gov.cn/quicksilver/public/plugin/getListPaneData.json?siteAreaId=402849d060a0d6720160a0d706600000&count=20&index=1',
        'http://kgxj.haikou.gov.cn/quicksilver/public/plugin/getListPaneData.json?siteAreaId=402849d060a0d6720160a0d9c953000f&count=20&index=1']

    def parse(self, response):
        item = {}

        textJson = json.loads(response.text)
        url = jsonpath.jsonpath(textJson, "$..id")
        for detailUrl in url:
            item['url'] = 'http://kgxj.haikou.gov.cn/quicksilver/public/plugin/detail.htm?id=' + detailUrl
            yield scrapy.Request(item['url'], callback=self.parse_info, meta={'item': copy.deepcopy(item)},
                                 dont_filter=True)

    def parse_info(self, response):
        item = response.meta['item']

        item['title'] = response.xpath('//*[@id="getTitle"]/text()').get().strip()

        item['cityId'] = 2257

        item['classifyId'] = ''

        item['administrativeId'] = ''

        html = etree.HTML(response.text)
        for elem in html.xpath('//style|//script'):
            elem.getparent().remove(elem)
        content = html.xpath("//*[@class='text_main']//text()")
        sss = ''
        for i in content:
            sss = sss + i
        # 去除
        item['content'] = sss.strip()
        # html标签
        div_data = html.xpath("//*[@class='text_main']")
        p_list = div_data[0].xpath('.//*')
        # 遍历所有的p标签，将里边的src,oldsrc属性拼接上前半部分
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
        compal = re.compile('style=".*?')
        item['contentHtml'] = re.sub(compal, '', contentHtml)
        # 时间
        pub_date = response.xpath("//*[contains(text(),'时间：')]").get()
        pub_date = re.findall('(20\d{2}-\d{2}-\d{2})', pub_date)[0]
        timeArray = time.strptime(pub_date, '%Y-%m-%d')
        timeStamp = int(time.mktime(timeArray)) * 1000
        item['publishTime'] = timeStamp
        # 新闻类型
        item['typeId'] = type_polic(item)
        # 来源
        item['sourceSite'] = '海口市科学技术局'
        # 行业
        item['industry'] = ''
        # 行业id
        item['industryId'] = ''

        # 附件名
        attachment_name = response.xpath('//*[@class="text"]/text()').getall()
        # 附件url
        attachment_url = response.xpath('//*[@class="text-a"]/@href').getall()
        # 整合name和url
        file_name = 'name'  # json 每一项中第一项的key
        file_url = 'url'  # json 每一项中第二项的key
        file_list = []
        for item1, item2 in zip(attachment_name, attachment_url):
            item2 = response.urljoin(item2)
            file_dic = {file_name: item1.strip(), file_url: item2.strip()}
            file_list.append(file_dic)
        item['attachments'] = file_list
        #print(item)
        yield item
