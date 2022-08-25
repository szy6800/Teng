import scrapy
import time
import re
from lxml import etree
import copy
from .msBureau import type_polic,index
import htmlmin



class GovSpider(scrapy.Spider):
    name = 'test'
    allowed_domains = ['changchun.gov.cn']
    start_urls = ['https://dev.kdlapi.com/testproxy']

    def parse(self, response):
        print(response.text)
