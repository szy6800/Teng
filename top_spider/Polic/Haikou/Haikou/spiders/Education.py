import copy
import re
import time

import scrapy
from lxml import etree

from .msBureau import type_polic

#教育局
class EducationSpider(scrapy.Spider):
    name = 'Education'
    allowed_domains = ['jyj.haikou.gov.cn']
    start_urls = [
        "http://jyj.haikou.gov.cn/edu/tzgg/list.action?shouye_biaozhi=%xxgk_id%&channelId=4767&pageNo=1&pageSize=25",
        "http://jyj.haikou.gov.cn/edu/zcjd/list.action?shouye_biaozhi=%xxgk_id%&channelId=4762&pageNo=1&pageSize=25",
        "http://jyj.haikou.gov.cn/edu/zxjd/list_wjk.action?shouye_biaozhi=%xxgk_id%&channelId=6603677&pageNo=1&pageSize=25"]

    # http://jyj.haikou.gov.cn/edu/tzgg/list.action?shouye_biaozhi='xxgk_id'&channelId=4767&pageNo=1&pageSize=25 # 公告公式 22
    # http://jyj.haikou.gov.cn/edu/zcjd/list.action?shouye_biaozhi='xxgk_id'&channelId=4762&pageNo=3&pageSize=25 # 政策文件 6
    # http://jyj.haikou.gov.cn/edu/zxjd/list_wjk.action?shouye_biaozhi='xxgk_id'&channelId=6603677&pageNo=1&pageSize=25 # 最新解读 1
    def parse(self, response):
        item = {}
        list_url = response.xpath('//*[@class="flfg_038-01"]//li/a/@href').getall()
        #print(list_url)

        for href in list_url:
            item['url'] = response.urljoin(href)
            yield scrapy.Request(item['url'], callback=self.parse_info, meta={'item': copy.deepcopy(item)},
                                 dont_filter=True)

    def parse_info(self, response):
        item = response.meta['item']

        item['title'] = response.xpath('//ucaptitle/text()').get().strip()

        item['cityId'] = 2257

        item['classifyId'] = ''

        item['administrativeId'] = ''

        # 正文
        # 去除js和css节点
        html = etree.HTML(response.text)
        for elem in html.xpath('//style|//script'):
            elem.getparent().remove(elem)
        content = html.xpath("//ucapcontent//text()")
        sss = ''
        for i in content:
            sss = sss + i
        # 去除
        item['content'] = sss.strip()
        # html标签
        div_data = html.xpath("//ucapcontent")
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
        pub_date = response.xpath("//*[@class='cy_ytbt']//*[contains(text(),'发布日期：')]").get()
        pub_date = re.findall('(20\d{2}-\d{2}-\d{2})', pub_date)[0]
        timeArray = time.strptime(pub_date, '%Y-%m-%d')
        timeStamp = int(time.mktime(timeArray)) * 1000
        item['publishTime'] = timeStamp
        # 新闻类型
        item['typeId'] = type_polic(item)
        # 来源
        item['sourceSite'] = '海口市教育局'
        # 行业
        item['industry'] = ''
        # 行业id
        item['industryId'] = ''
        # 附件名
        attachment_name = response.xpath('//*[@class="file_box"]//a/text()').getall()
        # 附件url
        attachment_url = response.xpath('//*[@class="file_box"]//a/@href').getall()
        # 整合name和url
        file_name = 'name'  # json 每一项中第一项的key
        file_url = 'url'  # json 每一项中第二项的key
        file_list = []
        for item1, item2 in zip(attachment_name, attachment_url):
            item2 = response.urljoin(item2)
            file_dic = {file_name: item1.strip(), file_url: item2.strip()}
            file_list.append(file_dic)
        item['attachments'] = file_list

        # print(item['attachments'])
        yield item
