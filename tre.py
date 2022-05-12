# -*- coding: utf-8 -*-

# @Time : 2022/4/19 21:24
# @Author : 石张毅
# @Site : 
# @File : tre.py
# @Software: PyCharm
import requests
import jsonpath
import json
for i in range(1,5):

    headers = {
        'Connection': 'keep-alive',
        'Accept': 'text/javascript, application/javascript, application/ecmascript, application/x-ecmascript, */*; q=0.01',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
        'Referer': 'http://ec.custeel.com/home/markList.html',
        'Accept-Language': 'zh-CN,zh;q=0.9',
    }

    params = (
        ('method', 'getBidsAlls'),
        ('tname', ''),
        ('cname', ''),
        ('putdate', ''),
        ('pageNum', '{}'.format(i)),
        ('pageSize', '20'),
        ('_', '1651226516714'),
    )

    response = requests.get('http://ec.custeel.com/cgnews.mv', headers=headers, params=params).json()
    print(response)
    # a = jsonpath.jsonpath(response, '$..bname')
    # print(a)
#NB. Original query string below. It seems impossible to parse and
#reproduce query strings 100% accurately so the one below is given
#in case the reproduced version is not "correct".
# response = requests.get('http://ec.custeel.com/cgnews.mv?method=getBidsAlls&callback=jQuery17205031662021907224_1651226489091&tname=&cname=&putdate=&pageNum=4&pageSize=20&_=1651226516714', headers=headers, cookies=cookies, verify=False)
