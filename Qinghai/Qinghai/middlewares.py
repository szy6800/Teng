# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html
import random
import re
import time
import requests
from requests.adapters import HTTPAdapter
from scrapy import signals
import logging  # 引入logging模块
import os.path
import time
import redis
from scrapy import signals
from scrapy.exceptions import IgnoreRequest
from urllib.parse import urlparse
from scrapy.http import HtmlResponse
from celery.worker.state import requests
from selenium import webdriver
from selenium.common.exceptions import TimeoutException

from Qinghai.settings import *


class QinghaiSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.
    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class QinghaiDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    @staticmethod
    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class RandomUserAgentMiddleware(object):
    def __init__(self):
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.835.163 Safari/535.1',
            'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0) Gecko/20100101 Firefox/6.0',
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
            'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)',
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER",
            "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; LBBROWSER)",
        ]

    def process_request(self, request, spider):
        request.headers['User-Agent'] = random.choice(self.user_agents)

    def process_exception(self, request, exception, spider):
        if isinstance(exception, TimeoutError):
            print('****************************请求超时****************************')
            return request

# # 第一步，创建一个logger
# logger = logging.getLogger()
# logger.setLevel(logging.INFO)  # Log等级总开关
# # 第二步，创建一个handler，用于写入日志文件
# rq = time.strftime('%Y%m%d%H%M', time.localtime(time.time()))
# log_path = os.path.dirname(os.getcwd()) + '/Logs/'
# log_name = log_path + rq + '.log'
# logfile = log_name
# fh = logging.FileHandler(logfile, mode='w')
# fh.setLevel(logging.DEBUG)  # 输出到file的log等级的开关
# # 第三步，定义handler的输出格式
# formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
# fh.setFormatter(formatter)
# # 第四步，将logger添加到handler里面
# logger.addHandler(fh)

from Qinghai.settings import PROXY_REDIS_IP, PROXY_REDIS_PORT, PROXY_REDIS_PASSWD

class RandomIPMiddleware(object):
    def __init__(self):
        self.pool2 = redis.ConnectionPool(
            host=PROXY_REDIS_IP, port=PROXY_REDIS_PORT, password=PROXY_REDIS_PASSWD, decode_responses=True
        )
        self.db2 = redis.Redis(connection_pool=self.pool2)
        # 获取所有ip返回列表
        result = self.db2.hgetall('localproxyip')
        print(result)
        self.ips = []
        for k, v in result.items():
            ip = k + ":" + v
            self.ips.append(ip)
        print(self.ips)

    def process_request(self, request, spider):
        try:
            # 此方法会返回一个随机ip ['ip']
            proxy = random.choices(self.ips)
            # proxy = ''
            if proxy:
                proxy = proxy[0]
                agreement = urlparse(request.url).scheme
                if agreement == 'http':
                    spider.logger.info('使用代理[%s]访问[%s]' % (proxy, request.url))
                    request.meta['proxy'] = 'http://' + proxy
                else:
                    spider.logger.info('使用代理[%s]访问[%s]' % (proxy, request.url))
                    request.meta['proxy'] = 'https://' + proxy
            else:
                spider.logger.warning('不使用代理访问[%s]' % request.url)
            return None
        except requests.exceptions.RequestException:
            spider.logger.error('ProxyIPMiddleware出错了! ')

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
        if isinstance(exception, TimeoutError):
            print('****************************请求超时****************************')
            return request
        # 出现异常时（超时）使用代理
        print("\n出现异常，正在使用代理重试....\n",exception)
        ip = random.choice(self.ips)
        # 对当前reque加上代理
        request.meta['proxy'] = 'https://' + ip
        return request

