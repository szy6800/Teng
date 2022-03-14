# -*- coding: utf-8 -*-

# @Time : 2022/3/3 17:21
# @Author : Szy
import requests


res = requests.get('https://www.mps.gov.cn/n2254314/n2254475/n2254481/index.html')
print(res.text)