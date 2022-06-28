import datetime
import redis
import random
import time
from requests.adapters import HTTPAdapter
from apscheduler.schedulers.blocking import BlockingScheduler
import requests


def get_daili(num=1, sheng='', port='1', time1=1, pack='238019'):
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


class Redis_Ip():

    def __init__(self):
        self.pool2 = redis.ConnectionPool(
            host='123.56.87.41', port=6379, password='$SMe9ndaZQw$4bJ2', decode_responses=True
        )
        self.db2 = redis.Redis(connection_pool=self.pool2)
        # 获取所有ip返回列表
        result = self.db2.hgetall('localproxyip')
        self.all_ip_list = [] # 用于存放从redis里的ip
        self.usable_ip_list = []  # 用于存放通过检测ip后是否可以使用
        self.dele_usable_ip_list = []  # 用于存放通过检测ip后不可使用的ip
        self.ip_nums = 40 # 定义redis库中可用ip数量
        for k, v in result.items():
            ip = k + ":" + v
            self.all_ip_list.append(ip)
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36',
            'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0) Gecko/20100101 Firefox/6.0',
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
            'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)',
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER",
            "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; LBBROWSER)",
        ]
    def request_header(self):
        headers = {
            # 'User-Agent': UserAgent().random #常见浏览器的请求头伪装（如：火狐,谷歌）
            'User-Agent': random.choice(self.user_agents)
        }
        return headers

    #发送请求，获得响应
    def send_request(self):
        #爬取7页，可自行修改
        for proxy in self.all_ip_list:
            Redis_Ip.test_ip(self, proxy)      #开始检测获取到的ip是否可以使用
        print(f'redis中的ip个数为：{len(self.all_ip_list)}')
        print(f'可以使用的ip个数为：{len(self.usable_ip_list)}')
        print(f'不可以使用的ip个数为：{len(self.dele_usable_ip_list)}')
        print('分别有：\n', self.usable_ip_list)
        print('分别有：\n', self.dele_usable_ip_list)
        if len(self.usable_ip_list) < self.ip_nums:
            ip_num = self.ip_nums - len(self.usable_ip_list)
            new_ips = get_daili(time1=1, num=ip_num)
            for newip in new_ips:
                new_ip = newip.split(':')
                self.db2.hset('localproxyip', new_ip[0], new_ip[1])
        for dele_usable in self.dele_usable_ip_list:
            dele_list = dele_usable.split(':')
            self.db2.hdel('localproxyip', dele_list[0])  # 将name对应的hash中指定key的键值对删除

    #检测ip是否可以使用
    def test_ip(self, proxy):
        #构建代理ip
        proxies = {
            "http": "http://" + proxy,
            "https": "https://" + proxy,
            # "http": proxy,
            # "https": proxy,
        }
        try:
            response = requests.get(url='http://ziliao.impk113.com/index.html',headers=Redis_Ip.request_header(self), proxies=proxies,timeout=5) #设置timeout，使响应等待1s
            response.close()
            if response.status_code == 200:
                self.usable_ip_list.append(proxy)
                print(proxy, '\033[31m<<<<<<ip可用>>>>>>\033[0m')
            else:
                print(proxy, '<<<<<<ip不可用>>>>>>,换网站测试')
                response = requests.get(url='http://www.baidu.com/s?ie=UTF-8&wd=ip',
                                        headers=Redis_Ip.request_header(self), proxies=proxies,
                                        timeout=5)  # 设置timeout，使响应等待1s
                response.close()
                if response.status_code == 200:
                    self.usable_ip_list.append(proxy)
                    print(proxy, '\033[31m<<<<<<ip可用>>>>>>\033[0m')
                else:
                    print(proxy, '<<<<<<ip不可用>>>>>>')
                    self.dele_usable_ip_list.append(proxy)
        except:
            print(proxy,'请求异常')
            self.dele_usable_ip_list.append(proxy)

def job():
    start_times = datetime.datetime.now()  # 采集开始时间
    start_time = str(start_times).split('.')[0]
    print('Starting time ===>', start_time)

    # 采集逻辑
    print('Bidding website data transfer =============>redis update!!!!')
    '''
    更新程序
    '''
    Redis_Ip().send_request()
    print('Collect again after 1 hour!!!!')
    end_time = str(datetime.datetime.now()).split('.')[0]  # 采集结束时间
    print(f"Starting time ===> {start_time}, End time ===> {end_time}")
    next_start_time = (start_times + datetime.timedelta(hours=1)).strftime('%Y/%m/%d %H:%M:%S')  # 下次采集间隔时间
    print('Next startup time =====>', next_start_time, '\n')


if __name__ == "__main__":
    Redis_Ip().send_request()
    '''定时器任务'''
    # scheduler = BlockingScheduler()  # 实例化定时器
    # scheduler.add_job(job, 'cron', hour=4, minute=55)
    # scheduler.add_job(job, 'cron', hour=5, minute=35)
    # scheduler.add_job(job, 'cron', hour=9, minute=55)
    # scheduler.add_job(job, 'cron', hour=10, minute=35)
    # scheduler.add_job(job, 'cron', hour=15, minute=55)
    # scheduler.add_job(job, 'cron', hour=16, minute=35)
    # scheduler.add_job(job, 'cron', hour=21, minute=55)
    # scheduler.add_job(job, 'cron', hour=22, minute=35)
    # # scheduler.add_job(job, 'cron', hour=23, minute=50)
    # try:
    #     scheduler.start()
    # except (KeyboardInterrupt, SystemExit):
    #     pass
    # except SystemExit:
    #     print('exit')
    #     exit()
