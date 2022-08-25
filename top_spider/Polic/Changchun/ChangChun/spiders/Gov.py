import scrapy
import time
import re
from lxml import etree
import copy
from .msBureau import type_polic,index
import htmlmin
# http://www.changchun.gov.cn/zw_33994/tzgg/index_9.html


class GovSpider(scrapy.Spider):
    name = 'Gov'
    allowed_domains = ['changchun.gov.cn']
    start_urls = ['http://www.changchun.gov.cn/zw_33994/tzgg/index.html']

    def parse(self, response):
        # print(response.text)
        item = {}
        list_url = response.xpath('//*[@class="xyh_listul"]//*[@class="currency_ul"]/li/a/@href').getall()
        for href in list_url:
            item['url'] = response.urljoin(href)
            yield scrapy.Request(item['url'],callback=self.parse_info, meta={'item': copy.deepcopy(item)},dont_filter=True)

    def parse_info(self, response):
        item = response.meta['item']

        item['title'] = response.xpath('//*[@class="xyh_xxynrq"]/h2/text()').get()

        item['cityId'] = 3519

        item['classifyId'] = ''
        # 大分类_id 人力
        item['administrativeId'] = ''
        # 正文
        # 去除js和css节点
        html = etree.HTML(response.text)
        for elem in html.xpath('//style|//script|//*[@id="div_div"]|//*[@class="print"]|//*[@id="Canvas"]'):
            elem.getparent().remove(elem)
        content = html.xpath("//*[contains(@class,'_Editor')]//text()")
        sss = ''
        for i in content:
            sss = sss + i
        # 去除
        item['content'] = sss.strip()

        #去 html标签
        div_data = html.xpath("//*[contains(@class,'_Editor')]")
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
        compal = re.compile('style=".*?"')
        item['contentHtml'] = re.sub(compal, '', contentHtml)
        # 时间
        pub_date = response.xpath("//*[contains(text(), '时间：')]").get()
        pub_date = re.findall('(20\d{2}-\d{2}-\d{2})', pub_date)[0]
        timeArray = time.strptime(pub_date, "%Y-%m-%d")
        timeStamp = int(time.mktime(timeArray)) * 1000
        item['publishTime'] = timeStamp
        print(item['publishTime'])

        # 新闻类型
        item['typeId'] = type_polic(item)
        # 来源
        item['sourceSite'] = '长春市人民政府'
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
        item['attachments'] = file_list

        yield item
