# -*- coding: utf-8 -*-

# @Author : 石张毅
# @Site : 比比招标网
# @introduce: https://www.bibenet.com/zbgsu5.html

import scrapy
import hashlib
#
class BiSpider(scrapy.Spider):
    name = 'bi'
    allowed_domains = ['bibenet.com']
    # 招标公告 50    5月23日
    start_urls = ['https://www.bibenet.com/zbggu630000u0u{}.html'.format(i) for i in range(1,2)]
    # 招标预告 15
    # start_urls = ['https://www.bibenet.com/zbygu630000u0u{}.html'.format(i) for i in range(1,9)]
    # 变更公告 74
    # start_urls = ['https://www.bibenet.com/bgggu630000u0u{}.html'.format(i) for i in range(40,74)]
    # 中标 40
    # start_urls = ['https://www.bibenet.com/zbgsu630000u0u{}.html'.format(i) for i in range(1,40)]

    def parse(self, response, *args, **kwargs):
        href = response.xpath('//a[@class="fl"]/@href').getall()
        titles = response.xpath('//a[@class="fl"]/text()').getall()
        types = response.xpath('//a[@class="fl"]/preceding::td[1]/text()').getall()
        pro_names = response.xpath('//a[@class="fl"]/following::td[1]/text()').getall()
        pubs = response.xpath('//a[@class="fl"]/following::td[2]/text()').getall()
        for href,titles,types,pro_names,pubs in zip(href,titles,types,pro_names,pubs):
            item = dict()
            item['id'] = href.strip()
            item['projectName'] = titles.strip()
            item['dataTypeStr'] = types.strip()
            item['prov_name'] = pro_names.strip()
            item['publishDate'] = pubs.strip()
            # item['code']
            check_md5 = item['projectName']+item['id']
            # 测试去重
            item['code'] = hashlib.md5(check_md5.encode(encoding='utf-8')).hexdigest()
            yield item
