# -*- coding: utf-8 -*-
import scrapy
import copy
import time,re
from lxml import etree
from .Market_text import *

class WjSpider(scrapy.Spider):
    name = 'Market'
    allowed_domains = ['scjgj.wuhan.gov.cn']
    # start_urls = ['http://scjgj.wuhan.gov.cn/zwgk_65/jggg/tzgg/index_{}.shtml'.format(i) for i in range(10,50)]



    def start_requests(self):
        for each in index():
            cate = each["cate"]
            pages = each["pages"]
            for p in range(pages):
                p = f"_{p}" if p else ""
                url = f"http://scjgj.wuhan.gov.cn/{cate}{p}.shtml"
                yield scrapy.Request(url=url, callback=self.parse, dont_filter=True)

    def parse(self, response):
        item = {}
        # # 反序列化
        list_url = response.xpath('//*[@id="share"]//a/@href|//*[@id="zcwj"]//a/@href').getall()
        # 循环遍历
        for href in list_url:
            item['url'] = response.urljoin(href)
            # print(item['url'])
            yield scrapy.Request(item['url'], callback=self.parse_info, meta={'item': copy.deepcopy(item)})

    def parse_info(self, response):

        item = response.meta['item']
        # 标题
        try:
            item['title'] = response.xpath("//*[@name='ArticleTitle']/@content").get()
            # 城市id
            item['cityId'] = 845

            item['classifyId'] = ''
            # 大分类
            item['big_type'] = ''
            # 大分类_id
            item['administrativeId'] = 1
            # 正文
            # 去除js和css节点和多余的文字
            html = etree.HTML(response.text)
            for elem in html.xpath('//style|//script|//*[@class="article-code"]|//h2|//*[@class="option clearfix"]|//*[@class="preview"]|//*[@class="table table-bordered"]'):
                elem.getparent().remove(elem)
            content = html.xpath('//*[@class="article"]//text()')
            sss = ''
            for i in content:
                sss = sss + i
            # 去除
            item['content'] = sss.strip()
            div_data = html.xpath('//*[@class="article"]')
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
            contentHtml = etree.tostring(div_data[0], encoding='utf-8').decode().replace('附件:', '')
            compal = re.compile('style=".*?"|http://scjgj.wuhan.gov.cn/govapp/lib/ueditor_demo/ueditor2/dialogs/attachment/fileTypeImages/.*?gif')
            contentHtml = re.sub(compal, '', contentHtml)
            try:
                tables = html.xpath('//*[@class="article"]//table/@width')[0]
                item['contentHtml'] = re.sub(tables, '', contentHtml)
            except:
                item['contentHtml'] = re.sub(compal, '', contentHtml)
            #时间

            pub_date = response.xpath("//*[@name='PubDate']/@content|//*[@name='pubdate']/@content").get()
            timeArray = time.strptime(pub_date, "%Y-%m-%d %H:%M")
            timeStamp = int(time.mktime(timeArray)) * 1000
            item['publishTime'] = timeStamp

            # 新闻类型
            item['typeId'] = type_polic(item)
            # 来源
            item['sourceSite'] = '武汉市市场监督管理局'
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
        except:
            print('这是一个文件！')