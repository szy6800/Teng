import copy
import re
import time

import scrapy
from lxml import etree


#税务局
from .msBureau import type_polic, method_name, methodNameUrl


class TaxSpider(scrapy.Spider):
    name = 'Tax'
    allowed_domains = ['hainan.chinatax.gov']
    # start_urls = ['http://hainan.chinatax.gov.cn/sxpd_1_6/index_{}.html'.format(i) for i in range(2, 132)]
    start_urls = ['http://hainan.chinatax.gov.cn/sxpd_1_6/index.html']

    def parse(self, response):
        item = {}
        list_url = response.xpath('//*[@class="mpgright_sum"]//ul/li/a/@href').getall()
        for href in list_url:
            item['url'] = response.urljoin(href)
            # print(item['url'])
            yield scrapy.Request(item['url'], callback=self.parse_info, meta={'item': copy.deepcopy(item)},
                                 dont_filter=True)

    def parse_info(self, response):
        item = response.meta['item']

        item['title'] = response.xpath('//*[@class="zx-xxxqy"]//h2/text()').get().strip()

        item['cityId'] = 2257

        item['classifyId'] = ''

        item['administrativeId'] = ''

        # 正文
        # 去除js和css节点
        html = etree.HTML(response.text)
        for elem in html.xpath('//style|//script'):
            elem.getparent().remove(elem)
        content = html.xpath("//*[@id='fontzoom']//text()")
        sss = ''
        for i in content:
            sss = sss + i
        # 去除
        item['content'] = sss.strip()
        # html标签
        div_data = html.xpath("//*[@id='fontzoom']")
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
        # 压缩
        # contentHtml = htmlmin.minify(contentHtml)
        # 去除标签中的样式 如字体中的font样式
        compal = re.compile('style=".*?"')
        item['contentHtml'] = re.sub(compal, '', contentHtml)
        # 时间
        pub_date = response.xpath("//*[contains(text(),'日期：')]").get()
        pub_date = re.findall('(20\d{2}-\d{2}-\d{2})', pub_date)[0]
        timeArray = time.strptime(pub_date, '%Y-%m-%d')
        timeStamp = int(time.mktime(timeArray)) * 1000
        item['publishTime'] = timeStamp
        # 新闻类型
        item['typeId'] = type_polic(item)
        # 来源
        item['sourceSite'] = '海口市税务局'
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
        #print(item)
        yield item
