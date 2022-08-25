# -*- coding: utf-8 -*-
import scrapy
import copy
import time,re
from lxml import etree

# http://shanghai.chinatax.gov.cn/zcfw/rdwd/index_31.html

class Wj2Spider(scrapy.Spider):
    name = 'question'
    allowed_domains = ['chinatax.gov.cn']
    # start_urls = ['http://www.1ppt.com/word/hetong/']
    # start_urls = ['http://shanghai.chinatax.gov.cn/zcfw/rdwd/index_{}.html'.format(i) for i in range(1, 34)]# 上海
    start_urls = ['https://shenzhen.chinatax.gov.cn/sztax/zcwj/rdwd/common_list_{}.shtml'.format(i) for i in range(6,50)]# 广东

    def parse(self, response):
        item = {}
        list_url = response.xpath('//*[@class="pageList infoList listContent"]//li//a/@href').getall()
        # print(list_url)
        # 循环遍历
        for href in list_url:
            # 原始链接
            item['url'] = response.urljoin(href)
            yield scrapy.Request(item['url'], callback=self.parse_down, meta={'item': copy.deepcopy(item)})

    def parse_down(self,response):
        item = response.meta['item']
        item['title'] = response.xpath("//*[@name='ArticleTitle']/@content").get().strip()
        item['times'] = response.xpath("//*[@name='PubDate']/@content").get().strip()
        content = response.xpath('//*[@class="content"]//text()').getall()
        sss = ''
        for i in content:
            sss = sss + i
        # 去除
        item['content'] = sss.strip()

        yield item











