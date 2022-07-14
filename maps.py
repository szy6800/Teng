# -*- coding: utf-8 -*-

# @Time : 2022/4/11 15:35
# @Author : 石张毅
# @Site : 
# @File : maps.py
# @Software: PyCharm 
import requests
from lxml import etree
url = 'http://www.iecity.com/CityList/map/'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36'
}
res = requests.get(url, headers=headers)
res.encoding = res.apparent_encoding
html = etree.HTML(res.text)

# 省份
provice = html.xpath('//*[@class="CityList"]//*[@class="Province"]/text()')
provices = html.xpath('//*[@class="CityList"]//*[@class="Province"]/following::ul[1]')

te = []
for i, i1 in zip(provices, provice):
    city_list = i.xpath('./li/a/text()')
    for i in city_list:
        item = dict()
        item['provice'] = i1
        item['city_list'] = i
        print(item)
        te.append(item)
# print(te)

