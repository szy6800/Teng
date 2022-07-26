
import json

from scrapy import Spider, Request, cmdline
from scrapy.cmdline import execute


import requests

cookies = {
    '4hP44ZykCTt5S': '5Jqk4uTfMdcm21mdg5zxMeKWfjJwK.e6UwVuKMpIp5VOTIyDDDL24XeK7YE4ALfgFWJOY24nBRSVBlK_eog07kG',
    'JSESSIONID': '02205FCAD47772341EC8400CC61C2306.tomcat2',
    '4hP44ZykCTt5T': 'nA5Q1GBpiJJk7tZcyxhRKMk.6HncRZpfFWf09EtwNeysGq4T1we.jQok8KNnuiq3Q26g8807GZ_36qicc2W7m8N6lRdzUPbEdvdbVJU3GE2EyFjD1rRLiGCr8JyrYqfOHEq_bek5ymk6HMMPrGrOilXJwE1v6MbFMbHkOv0BVeU8GBOJT8i0yelRB9mEM7mICpilbT9LDQ.YK5L9GXGUgVhlOEj3PbRgmoxe5gEoOrQze5w8x8dnr8OJHbQG0ULAExkRfGLo7L4yYsiXX3L82e.qWSRGyxg3pmbAT7y8UXQiC0EwR76.mRfV1sSBcf7cmsotsAlbWXM2ZWpeUDdj7LHon6FgIqAJj1YS4_0LnIWcIwIZNaFU9dD2VBmD9V4b8X_h2CVSBshmrN8N1YNCNa',
}

headers = {
    'Connection': 'keep-alive',
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Referer': 'http://www.ccgp-gansu.gov.cn/web/doSearchmxarticlelssj.action?limit=20&start=40',
    'Accept-Language': 'zh-CN,zh;q=0.9',
}

params = (
    ('limit', '20'),
    ('start', '60'),
)

response = requests.get('http://www.ccgp-gansu.gov.cn/web/doSearchmxarticlelssj.action', headers=headers, params=params, cookies=cookies, verify=False)
print(response.text)
#NB. Original query string below. It seems impossible to parse and
#reproduce query strings 100% accurately so the one below is given
#in case the reproduced version is not "correct".
# response = requests.get('http://www.ccgp-gansu.gov.cn/web/doSearchmxarticlelssj.action?limit=20&start=60', headers=headers, cookies=cookies, verify=False)
