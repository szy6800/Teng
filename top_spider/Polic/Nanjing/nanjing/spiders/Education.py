# -*- coding: utf-8 -*-
import scrapy
import time
import re
from lxml import etree
import copy,jsonpath,json
from .wj_text import type_polic, index

# http://edu.nanjing.gov.cn/njsjyj/?id=xxgkgknr
class Wj4Spider(scrapy.Spider):
    name = 'Education'
    allowed_domains = ['njkl.gov.cn']
    start_urls = ['http://edu.nanjing.gov.cn/igs/front/search/publish/data/list.html?&index=wzqsearch-v20190124&type=infomation&siteId=53&pageSize=20&orderProperty=DOCRELTIME&pageIndex=3&orderDirection=desc&filter%5BSITEID%5D=53&filter%5BCHANNELID%5D=&filter%5BGROUPCAT%5D=214%2C215%2C216%2C217%2C394%2C397%2C2604%2C396%2C398%2C400%2C401%2C402%2C403%2C404%2C405%2C406%2C222%2C408%2C409%2C410%2C411%2C412%2C223%2C413%2C414%2C415%2C416%2C417%2C513%2C418%2C419%2C420%2C421%2C422%2C423%2C424%2C425%2C426%2C218%2C2571%2C219%2C220%2C224%2C225%2C1849%2C1848%2C1847%2C226%2C227%2C228%2C229%2C230%2C231%2C232%2C233%2C234%2C2005%2C294%2C2008%2C2009%2C2006%2C2033%2C2034%2C2011%2C2010%2C383%2C384%2C385%2C236%2C237%2C238%2C239%2C240%2C241%2C242%2C243%2C244%2C245%2C246%2C2570%2C2568%2C247%2C2049%2C249%2C250%2C251%2C252%2C253%2C254%2C255%2C256%2C257%2C258%2C259%2C260%2C261%2C262%2C522%2C264%2C265%2C263%2C520%2C521%2C266%2C267%2C2572%2C268%2C269%2C270%2C271%2C272%2C273%2C274%2C275%2C1895%2C514%2C276%2C515%2C516%2C517%2C277%2C278%2C279%2C280%2C284%2C285%2C286%2C287%2C301%2C306%2C307%2C308%2C309%2C310%2C311%2C312%2C313%2C314%2C315%2C316%2C317%2C510%2C323%2C324%2C325%2C326%2C327%2C328%2C329%2C330%2C331%2C332%2C333%2C334%2C336%2C337%2C338%2C339%2C340%2C341%2C342%2C343%2C344%2C511%2C345%2C346%2C347%2C348%2C349%2C350%2C351%2C352%2C353%2C354%2C355%2C356%2C357%2C358%2C359%2C360%2C361%2C362%2C363%2C364%2C365%2C366%2C367%2C368%2C512%2C369%2C370%2C371%2C372%2C373%2C374%2C375%2C376%2C377%2C378%2C379%2C380%2C381%2C235%2C386%2C387%2C1839%2C388%2C389%2C390%2C391%2C392%2C393%2C759%2C1842%2C2062%2C2063%2C2546%2C2561%2C427&pageNumber={}'.format(i) for i in range(1, 2)]

    def parse(self, response):
        # print(response.text)
        item = {}
        text = json.loads(response.text)
        list_url = jsonpath.jsonpath(text, '$..DOCPUBURL')
        # 循环遍历
        for href in list_url:
            # print(response.urljoin(href))
            item['url'] = response.urljoin(href.strip())
            yield scrapy.Request(item['url'], callback=self.parse_info, meta={'item': copy.deepcopy(item)},
                                 dont_filter=True)

    def parse_info(self, response):
        item = response.meta['item']
        # 标题
        item['title'] = response.xpath("//title/text()").get().strip()
        # 城市id 2293
        item['cityId'] = 2293

        item['classifyId'] = 9
        # 大分类_id 人力
        item['administrativeId'] = ''
        # 正文
        # 去除js和css节点
        html = etree.HTML(response.text)
        for elem in html.xpath('//style|//script|//*[@id="div_div"]|//*[@class="print"]|//*[@id="Canvas"]'):
            elem.getparent().remove(elem)
        content = html.xpath("//*[@class='con']/div//text()")
        sss = ''
        for i in content:
            sss = sss + i
        # 去除
        item['content'] = sss.strip()
        div_data = html.xpath("//*[@class='con']")
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
        contentHtml = etree.tostring(div_data[0], encoding='utf-8').decode().replace('附件：', '')
        compal = re.compile('style=".*?"|http://amr.ah.gov.cn/assets/images/files2/.*?gif|face=".*?"')
        contentHtml = re.sub(compal, '', contentHtml)
        try:
            tables = html.xpath('//*[@class="con"]//table/@width')[0]
            item['contentHtml'] = re.sub(tables, '', contentHtml)
        except:
            item['contentHtml'] = re.sub(compal, '', contentHtml)

        pub_date = response.xpath("//*[contains(text(),'生成日期：')]/following::td[1]/text()").get().strip()
        timeArray = time.strptime(pub_date, "%Y-%m-%d")
        timeStamp = int(time.mktime(timeArray)) * 1000
        item['publishTime'] = timeStamp
        # 新闻类型
        item['typeId'] = type_polic(item)
        # 来源
        item['sourceSite'] = '南京市教育局'
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

