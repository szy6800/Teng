# -*- coding: utf-8 -*-

# @Time : 2022/4/19 21:24
# @Author : 石张毅
# @Site : 
# @File : tre.py
# @Software: PyCharm 
import requests

import requests

headers = {
    'Connection': 'keep-alive',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="98", "Google Chrome";v="98"',
    'Accept': 'application/json, text/plain, */*',
    'Content-Type': 'application/json',
    'Hash': '0c2fa1a0e28aac8fb8de34c20e4d6b058b7c198505640d67fd142f65326f7ae7',
    'sec-ch-ua-mobile': '?0',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36',

}

data = '{"pageNum":4,"pageSize":10,"xzqDm":"63","startDate":"","endDate":""}'

response = requests.post('https://api.landchina.com/tGdxm/result/list', headers=headers, data=data)
print(response.text)