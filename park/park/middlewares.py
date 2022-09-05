# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals

# useful for handling different item types with a single interface
# from itemadapter import is_item, ItemAdapter
import random
import redis
import time
from requests.adapters import HTTPAdapter
import requests
from urllib.parse import urlparse
from scrapy.http import HtmlResponse
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from park.settings import PROXY_REDIS_IP, PROXY_REDIS_PORT, PROXY_REDIS_PASSWD

class ParkSpiderMiddleware:
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

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
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


class ParkDownloaderMiddleware:
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

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)




class RandomUserAgentMiddleware(object):
    def __init__(self):
        self.user_agents = [
                    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36'
        ]

    def process_request(self, request, spider):
        request.headers['user-agent'] = random.choice(self.user_agents)

    def process_exception(self, request, exception, spider):
        if isinstance(exception, TimeoutError):
            print('****************************请求超时****************************')
            return request




class RandomIPMiddleware(object):
    def __init__(self):
        self.pool2 = redis.ConnectionPool(
            host=PROXY_REDIS_IP, port=PROXY_REDIS_PORT, password=PROXY_REDIS_PASSWD, decode_responses=True
        )
        self.db2 = redis.Redis(connection_pool=self.pool2)
        # 获取所有ip返回列表
        result = self.db2.hgetall('localproxyip')
        self.ips = []
        for k, v in result.items():
            ip = k + ":" + v
            self.ips.append(ip)
        self.page = 0
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

            res = urlparse(request.url)  # 获取访问链接
            link = res.scheme + '://' + res.netloc  # 访问页面的域名
            self.db2.hset('jiankong', link, '0')
            # self.page = 0
            return None
        except requests.exceptions.RequestException:
            spider.logger.error('ProxyIPMiddleware出错了! ')


    def process_response(self, request, response, spider):
        # 对返回的response处理
        # 如果返回的response状态不是200，重新生成当前request对象
        if response.status != 200:
            self.page += 1  # 访问个数
            res = urlparse(request.url)  # 获取访问链接
            link = res.scheme + '://' + res.netloc  # 访问页面的域名
            self.db2.hset('jiankong', link, str(self.page))
            if self.page == 100:
                print('<<<<更换ip>>>>')
                result = self.db2.hgetall('localproxyip')
                self.ips = []
                self.page = 0
                for k, v in result.items():
                    ip = k + ":" + v
                    self.ips.append(ip)
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
        print("\n出现异常，正在使用代理重试....\n", exception)
        self.page += 1  # 访问个数
        res = urlparse(request.url)  # 获取访问链接
        link = res.scheme + '://' + res.netloc  # 访问页面的域名
        self.db2.hset('jiankong', link, str(self.page))
        if self.page == 30:
            print('<<<<更换ip>>>>')
            result = self.db2.hgetall('localproxyip')
            self.ips = []
            self.page = 0
            for k, v in result.items():
                ip = k + ":" + v
                self.ips.append(ip)
        ip = random.choice(self.ips)
        # 对当前reque加上代理
        request.meta['proxy'] = 'https://' + ip
        return request


class IPProxyDownloadMiddleware(object):
    def process_request(self, request, spider):
        proxy = "http://101.89.207.178:20444"
        request.meta['proxy'] = proxy
