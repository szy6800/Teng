# -*- coding: utf-8 -*-
import json

import jsonpath
import scrapy
import time
import re
from lxml import etree
import copy
from .wj_text import type_polic, index


class WjSpider(scrapy.Spider):
    name = 'test'
    allowed_domains = ['hunan.gov.cn']
    start_urls = ['https://api.yqypt.com/v2/policies/with_content?pageNum=4&pageSize=10&sort=RELEVANCY&industryId=0&policyClassifyId=0&policyTypeId=0&cityId=&keywords=%E7%99%BB%E8%AE%B0%E6%B3%A8%E5%86%8C']  # 30



