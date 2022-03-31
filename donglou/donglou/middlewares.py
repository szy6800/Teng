import random
import re
import redis
from scrapy import signals



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
        # result = ['119.5.181.235:4213', '175.167.20.63:4231', '42.56.237.67:4278', '112.194.88.39:4245', '42.85.232.220:4256', '220.201.87.15:4253', '175.155.49.130:4258', '113.237.230.141:4231', '221.10.104.5:4231', '42.57.88.87:4231', '114.250.162.241:4231', '183.95.162.214:4231', '113.235.170.89:4278', '58.19.83.134:4245', '42.177.136.95:4285', '175.174.142.58:4231', '175.155.141.243:4256', '116.115.209.41:4231', '42.57.90.160:4253', '1.29.109.57:4231', '42.56.239.220:4231', '58.243.29.131:4213', '116.138.246.103:4230', '175.155.142.0:4256', '58.243.28.189:4213', '58.243.29.163:4213', '175.146.208.251:4256', '1.25.144.192:4234', '42.56.238.122:4231', '58.243.29.11:4254', '112.194.90.34:4245', '58.19.13.14:4245', '221.202.131.15:4256', '114.250.167.199:4231', '112.195.154.146:4256', '183.95.163.173:4231', '113.57.35.60:4245', '42.56.239.118:4256', '221.199.64.45:4213', '221.202.99.116:4210', '114.250.168.138:4231', '58.243.28.197:4213', '116.115.208.140:4231', '125.36.206.16:4210', '124.94.184.46:4280', '183.92.12.114:4220', '123.8.95.174:4231', '113.57.57.150:4245', '221.203.150.132:4250', '111.161.152.130:4210']
        self.ips = ['42.7.28.236:4231', '221.199.195.34:4231', '124.230.9.218:4231', '175.173.222.46:4210', '113.235.73.21:4213']
        # for ips in result.strip().split('\n'):
        #     # ip = k + ":" + v
        #     self.ips.append(ips)
        # print(self.ips)

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