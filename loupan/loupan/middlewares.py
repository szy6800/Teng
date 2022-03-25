# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

import random
import re
import random
import re
import time
import requests
from requests.adapters import HTTPAdapter
from scrapy import signals

def get_daili(num=1, sheng='', port='1', time1=1, pack='221123'):
 # time:1 5-25min 2 25min-3h 3 3-6h 4 6-12h
 # port IP协议 1:HTTP 2:SOCK5 11:HTTPS
 # mr 去重选择（1:360天去重 2:单日去重 3:不去重）
 # pack=221123
 while 1:
  try:
   url = 'http://webapi.http.zhimacangku.com/getip?num=%s' % num + (
           '&type=1&pro=%s' % sheng + '&city=0&yys=100026&port=%s&time=%s' % (port, time1)) + (
                 '&ts=0&ys=0&cs=0&lb=1&sb=0&pb=4&mr=2&regions=&pack=%s' % pack)
   s1 = requests.Session()
   s1.mount('https://', HTTPAdapter(max_retries=3))
   content = s1.get(url, timeout=2).text
   ip_list = content.split('\r\n')[0:-1]
   ip_list2 = []
   for ip in ip_list:
    ip_list2.append(ip)
    # ip_list2.append({'https': ip, 'http': ip})
   print('代理IP:', ip_list2)
   time.sleep(1.2)
   break
  except Exception as e:
   time.sleep(2)
   print(e)
   continue

 return ip_list2
class RandomUserAgentMiddleware(object):
    def __init__(self):

        self.user_agents = [
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.835.163 Safari/535.1',
            'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0) Gecko/20100101 Firefox/6.0',
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
            'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)',
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER",
            "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; LBBROWSER)",
            "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36"
        ]

    def process_request(self, request, spider):
        request.headers['User-Agent'] = random.choice(self.user_agents)

    def process_exception(self, request, exception, spider):
        if isinstance(exception, TimeoutError):
            print('****************************请求超时****************************')
            return request


class RandomIPMiddleware(object):
    def __init__(self):
        # 获取所有ip返回列表
        result = ''''''
        self.ips = get_daili(time1=1, num=3)
        # self.ips = ['42.59.103.192:4231', '113.237.0.97:4256', '175.147.118.205:4213', '124.94.252.221:4213', '112.194.88.40:4245', '121.29.82.77:4231','116.115.208.253:4231', '218.24.54.115:4275', '113.237.0.58:4256']
        for ips in result.strip().split('\n'):
            # ip = k + ":" + v
            self.ips.append(ips)
        print(self.ips)

    def process_request(self, request, spider):

        ip = random.choice(self.ips)
        print('当前IP***：', ip)
        request.meta['proxy'] = 'http://' + ip

    def process_response(self, request, response, spider):
        # 对返回的response处理
        # 如果返回的response状态不是200，重新生成当前request对象
        if response.status != 200:

            ip = random.choice(self.ips)
            print("this is response !=200 ip:" + ip)
            request.meta['proxy'] = 'http://' + ip
            return request
        return response

    def process_exception(self, request, exception, spider):
        erro = str(exception)
        print(erro)
        chlid = re.search(r'chlid=(\d+)&', erro)
        if chlid:
            chlid = chlid.group(1)
            print(chlid)
            # self.db.sadd('chongshi_id', chlid)
        if isinstance(exception, TimeoutError):
            print('****************************请求超时****************************')

            return request
        # 出现异常时（超时）使用代理
        print("\n出现异常，正在使用代理重试....\n")
        ip = random.choice(self.ips)
        # 对当前reque加上代理
        request.meta['proxy'] = 'http://' + ip

        return request