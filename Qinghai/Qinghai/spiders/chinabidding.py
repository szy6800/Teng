import scrapy
import copy


from Qinghai.tools.utils import Utils_
from Qinghai.tools.DB_mysql import *
from Qinghai.tools.re_time import Times
import datetime
from Qinghai.tools.uredis import Redis_DB

class ChinabiddingSpider(scrapy.Spider):
    name = 'chinabidding'
    allowed_domains = ['baidu.com']
    # start_urls = ['http://baidu.com/']

    def __init__(self, *args, **kwargs ):
        super(ChinabiddingSpider, self).__init__()
        self.cates = [
            {"cate": "0", "pages": 50},  # 招标公告
            {"cate": "1", "pages": 3},  # 招标公告
            {"cate": "2", "pages": 50},  # 招标公告
            # {"cate": "3", "pages": 50},  # 招标公告
        ]
        self.t = Times()
        self.c_time = datetime.datetime.utcnow() - datetime.timedelta(days=3)

    def start_requests(self):
        for each in self.cates:
            cate = each["cate"]
            pages = each["pages"]
            for p in range(1, pages):
                # p = f"_{p+1}" if p else ""
                url = f"http://www.chinabidding.org.cn/BidInfoList_id_{p}_ty_{cate}.html"
                yield scrapy.Request(url=url, callback=self.parse,dont_filter=True)

    def parse(self, response):
        # print(response.text)
        item = {}
        # 列表页链接和发布时间
        list_url = response.xpath('//*[@id="hd"]//following::table[1]//td/a/@href').getall()
        titles = response.xpath('//*[@id="hd"]//following::table[1]//td/a/text()').getall()

        pub_times = response.xpath('//*[@id="hd"]//following::table[1]//td/a/following::td[1]/text()').getall()
        #循环遍历
        for href ,pub_time in zip(list_url, pub_times):
            # print(response.urljoin(href))
            item['link'] = response.urljoin(href.strip())
            pub_time = pub_time.replace('/','-')
            PUBLISH = self.t.datetimes(pub_time.strip())
            item['publish_time'] = PUBLISH.strftime('%Y-%m-%d')  # 发布时间
            # print(item['link'], item['publish_time'],item['title'])
            ctime = self.t.datetimes(item['publish_time'])

            item['uid'] = 'zf' + Utils_.md5_encrypt(item['link'] + item['publish_time'])
            if Redis_DB().Redis_pd(item['uid']) is True:  # 数据去重
                print(item['uid'], '\033[0;35m <=======此数据已采集=======> \033[0m')
                return
            if ctime < self.c_time:
                print('文章发布时间大于规定时间，不予采集', item['link'])
                return
            yield scrapy.Request(item['link'], callback=self.parse_info, meta={'item': copy.deepcopy(item)},dont_filter=True)

    @staticmethod
    def parse_info(response):
        if response.status != 200:
            return
        item = response.meta['item']
        # 标题
        item['title'] = response.xpath('//*[@id="cphMain_tle"]/text()').get()
        item['uuid'] = ''

        item['intro'] = ''
        item['abs'] = '1'
        from lxml import etree
        html = etree.HTML(response.text)
        div_data = html.xpath('//*[@class="doutline"]')
        item['content'] = etree.tostring(div_data[0], encoding='utf-8').decode()
        # 购买人
        item['purchaser'] = ''
        item['create_time'] = str(datetime.datetime.now().strftime('%Y-%m-%d'))
        # 代理人
        item['proxy'] = ''

        item['update_time'] = ''

        item['deleted'] = ''
        # 省 份
        item['province'] = response.xpath('//*[@id="dtr"]/text()').get().strip()
        # 基础
        item['base'] = ''

        item['type'] = response.xpath('//*[@id="navbar"]/a[last()]/text()').get().strip()
        # 行业
        item['items'] = response.xpath('//*[@id="fld"]/text()').get().strip()
        # 类型编号
        item['data_source'] = '00303'
        item['end_time'] = ''
        item['status'] = ''
        # 采购编号
        item['serial'] = response.xpath('//*[@id="bidNo"]/text()').get()

        yield item
