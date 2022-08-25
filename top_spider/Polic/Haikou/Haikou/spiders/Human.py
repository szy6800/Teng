import copy
import re
import sys
import time
import scrapy
#人力资源和社会保障局
from lxml import etree
from .msBureau import indexHuman, type_polic, method_name, methodNameUrl


# 人力资源和社会保障局
class HumanSpider(scrapy.Spider):
    name = 'Human'
    allowed_domains = ['haikou.gov.cn']
    # start_urls = ['http://haikou.gov.cn/']
    def start_requests(self):
        for each in indexHuman():
            cate = each['cate']
            pages = each['pages']
            for p in range(pages):
                p = f"_{p}" if p else ""
                url = f"http://rsj.haikou.gov.cn/{cate}index{p}.html"
                yield scrapy.Request(url=url, callback=self.parse, dont_filter=True)


    def parse(self, response):
        item = {}

        list_url = response.xpath('//*[@class="list-right_title"]/a/@href').getall()
        for href in list_url:
            item['url'] = response.urljoin(href)
            #print(item['url'])
            yield scrapy.Request(item['url'], callback=self.parse_info, meta={'item': copy.deepcopy(item)},
                                 dont_filter=True)

    def parse_info(self, response):
        item = response.meta['item']

        item['title'] = response.xpath('//*[@class="title_cen mar-t2"]/h2/text()').get().strip()

        item['cityId'] = 2257

        item['classifyId'] = ''

        item['administrativeId'] = ''

        # 去除 正文js和css的节点
        html = etree.HTML(response.text)
        for elem in html.xpath('//style|//script'):
            elem.getparent().remove(elem)
        content = html.xpath("//*[@id='zoom']//text()")
        sss = ''
        for i in content:
            sss = sss + i
        #去除
        item['content'] = sss.strip()
        # html标签
        div_data = html.xpath("//*[@id='zoom']")
        p_list = div_data[0].xpath('.//*')
        #遍历所有的p标签，将里边的src,oldsrc属性拼接上前半部分
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
        #去除标签中的样式 如字体中的font样式
        compal = re.compile('style=".*?')
        item['contentHtml'] = re.sub(compal, '', contentHtml)
        #时间
        pub_date = response.xpath('//*[@class="time"]/text()').get().strip()
        try:
            timeArray = time.strptime(pub_date, '%Y-%m-%d %H:%M:%S')
        except:
            timeArray = time.strptime(pub_date, '%Y-%m-%d')
        timeStamp = int(time.mktime(timeArray)) * 1000
        item['publishTime'] = timeStamp
        # 新闻类型
        item['typeId'] = type_polic(item)
        # 来源
        item['sourceSite'] = '海口市市场监督管理局'
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
       # print(item)
        yield item
