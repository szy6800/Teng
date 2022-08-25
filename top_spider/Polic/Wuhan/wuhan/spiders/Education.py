# -*- coding: utf-8 -*-
import scrapy
import time
import re
from lxml import etree
import copy
from .Economics_text import *
import json
import jsonpath
# http://czj.wuhan.gov.cn/BMDT/TZGG/index_1.html


class WjSpider(scrapy.Spider):
    name = 'Education'
    allowed_domains = ['wuhan.gov.cn']

    # headers = {
    #     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36",
    # }

    def start_requests(self):
        url = 'http://httpbin.org/get'
        yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        print(response.text)
        # str_text = json.loads(response.text)
        # proxy_ip = jsonpath.jsonpath(str_text, '$..origin')
        # print(proxy_ip)


