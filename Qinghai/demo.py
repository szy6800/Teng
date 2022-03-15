# -*- coding: utf-8 -*-

# @Time : 2022/3/11 18:06
# @Author : 石张毅
# @Site : 
# @File : demo.py
# @Software: PyCharm 

# !/usr/bin/env python
# coding:utf-8
"""
  Author:  chen_zj --<>
  Purpose:
  Created: 2021/09/06
"""

import re
import math
import time

import os
import requests
import pyquery
from multiprocessing import Process
import pickle
import json
# from retry import retry
from hashlib import md5

from ProcessTools import MultiProcess, ProcessManager
import shutil
import csv
from urllib import parse
from selenium import webdriver

from multiprocessing import Process

# import logging
# logging.basicConfig(level=logging.DEBUG,format='%(asctime)s - %(levelname)s: %(message)s')

# logger = logging.getLogger()
# logger.setLevel(logging.INFO)


headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
           'Accept-Language': 'zh-CN,zh;q=0.9',
           'Content-Type': 'image/gif',
           'Connection': 'keep-alive',
           'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}

info = """accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
accept-encoding: gzip, deflate, br
accept-language: zh-CN,zh;q=0.9
cache-control: max-age=0
cookie: PHPSESSID=7d2p2b1hoph6ol8r8bstmo8895; device-id=bac03f40-e215-4e4e-a5f9-b0040b3587fa; _ga=GA1.2.1144915757.1630392695; _gid=GA1.2.379321941.1630392695; _gcl_au=1.1.2055074178.1630392695; last-known-device-id=bac03f40-e215-4e4e-a5f9-b0040b3587fa; __cf_bm=c0455c573f6164a5e7dda09b535a111e9c200956-1630400606-1800-AbYn1EXIZU63F5i81erfqltF970jpjF228beVc2HsJ+xsmyzHISFGtOUzLTgYNszVGAnjzO5tM0DJ2gYj7A6L3yBi0miv1GinkhHTs4PCWgI+3hfW9tZA3oBOvO9LL/kVsTbzI+bvPRr1il+GROltkBShd0ks+PpSPh8SwBbmypz; AMP_TOKEN=%24NOT_FOUND; _gat=1; _gat_UA-74882607-5=1
sec-ch-ua: "Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"
sec-ch-ua-mobile: ?0
sec-fetch-dest: document
sec-fetch-mode: navigate
sec-fetch-site: none
sec-fetch-user: ?1
upgrade-insecure-requests: 1
user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36"""

headers = {}
for i in info.split('\n'):
    a = i.split(': ', 1)
    headers[a[0]] = a[1]

session = requests.Session()
session.headers = headers


def downloadPageOld(data):
    path = data['path']
    url = data['url']
    f = session.get(url)
    open(path, 'wb').write(f.content)
    return f.content


# options = webdriver.ChromeOptions()
# options.add_argument('--headless')
# browser = webdriver.Chrome(executable_path='/Users/chen_zj/Downloads/chromedriver',chrome_options=options)


def downloadPage(data):
    # 下载测试

    # 每次新建一个chrome进行网页访问，获取页面内容后，关闭驱动
    path = data['path']
    url = data['url']
    # options = webdriver.ChromeOptions()
    # options.add_argument('--headless')
    # browser = webdriver.Chrome(executable_path='/Users/chen_zj/Downloads/chromedriver',chrome_options=options)
    # browser = webdriver.Chrome(executable_path='/Users/chen_zj/Downloads/chromedriver')

    f = browser.get(url)
    content = browser.page_source
    open(path, 'w').write(content)
    # browser.close()
    browser.delete_all_cookies()
    time.sleep(1)
    return content


class MultiProcessV1(Process):
    def __init__(self, ind, data, func, iswrite=False):
        super(MultiProcessV1, self).__init__()
        self.ind = ind
        self.data = data
        self.func = func
        self.iswrite = iswrite

        self.browser = ''
        self.browserReload()

        if self.iswrite:
            if not os.path.exists('outdata'):
                os.mkdir('outdata')

    def browserReload(self):
        # 初始化驱动
        try:
            self.browser.quit()
        except:
            pass

        options = webdriver.ChromeOptions()
        # options.add_argument('--headless')  # 是否使用无头模式
        self.browser = webdriver.Chrome(executable_path='/Users/chen_zj/Downloads/chromedriver', chrome_options=options)
        self.browser.set_window_size(512, 480)
        time.sleep(1)

    def downloadPage(self, data):
        path = data['path']
        url = data['url']
        f = self.browser.get(url)
        time.sleep(1)  # 加入延时
        content = self.browser.page_source
        if len(content) > 10000:
            open(path, 'w').write(content)  # 如果数据非空，就写出
        else:
            print(data)
            self.downloadPage(data)  # 如果返回未查询结果，则利用递归，重复采集该链接

        self.browser.delete_all_cookies()  # 每次都清理所有cookies,防止页面在浏览器记录内容

        return content

    def run(self):
        print('start')
        alldata = []
        c1 = 0
        size = len(self.data)
        start = time.time()
        for tmp in self.data:
            c1 += 1
            if 1:
                d = self.downloadPage(tmp)  # 使用自身的downloadPage进行页面下载
                if '我们的系统检测到您的计算机网络中存在异常流量' in d:
                    raise ('内部检测')
                    # break
                if 1:
                    alldata.append(d)

            if c1 % 100 == 0:
                use = time.time() - start
                st = 'Process:%s Completed:%.4f Size:%s Finished:%s Timeuse:%.4f Estimated:%.4f' % (self.ind,
                                                                                                    c1 / size,
                                                                                                    size, c1, use,
                                                                                                    size / c1 * use)
                # print(self.ind,'%s'%(c1/size),use,size/c1*use)
                print(st)
                # self.browserReload()

            if c1 % 10000 == 9999 and self.iswrite:
                out = open('outdata/data_%s_%s.pickle' % (self.ind, time.time()), 'wb')
                pickle.dump(alldata, out)
                out.close()
                alldata = []

        if self.iswrite:
            out = open('outdata/data_%s_%s.pickle' % (self.ind, time.time()), 'wb')
            pickle.dump(alldata, out)
            out.close
        use = time.time() - start
        st = 'Process:%s Completed:%.4f Size:%s Finished:%s Timeuse:%.4f Estimated:%.4f' % (self.ind,
                                                                                            c1 / size,
                                                                                            size, c1, use,
                                                                                            size / c1 * use)
        print(st)


def ProcessManagerV1(L, func, num=8, iswrite=False):
    if not os.path.exists('outdata'):
        os.mkdir('outdata')
    print(len(L))
    t = len(L)
    start = time.time()
    # num = 8
    inteval = len(L) // num + 1
    Lis = []
    for i in range(num):
        s1 = L[i * inteval:(i + 1) * inteval]
        p = MultiProcessV1(i, s1, func, iswrite)
        Lis.append(p)
        p.daemon = True
        p.start()
    for i in Lis:
        i.join()

    use = time.time() - start
    print('time used :', use)


def getAlllink():
    f = open('在世人物-中文wiki.csv')
    reader = csv.reader(f)
    head = reader.__next__()
    L = []
    for ar in reader:
        name = ar[1]
        L.append(name)

    S = set(L)
    L = []
    for i in S:

        url = 'https://www.qcc.com/web/search?key=%s' % i
        path = 'html/%s.html' % i
        if os.path.exists(path):
            continue
        d = {'url': url, 'path': path}
        L.append(d)

    # for i in L:
    #    print(i)
    #    downloadPage(i)
    ProcessManagerV1(L, downloadPage, 4)


def parseHTML(path):
    # 解析页面
    '''
    f = open(path).read()
    py = pyquery.PyQuery(f,parser='html')
    div = py('.person')
    L = []
    for i in range(len(div)):


        name = div.eq(i)('.name').eq(0).text()
        age = div.eq(i)('.age').eq(0).text()
        location = div.eq(i)('.location').eq(0).text()
        relatives = div.eq(i)('.relatives').eq(0).text()

        one = [name,age,location,relatives]
        L.append(one)
    return L
    '''
    pass


def formatData():
    # 格式化数据
    '''
    out = open('data.csv','w',encoding='utf8')
    writer = csv.writer(out)
    title = ['姓名','年龄','曾住地','可能的亲戚']
    writer.writerow(title)
    L = os.listdir('html')
    for i in L:
        if not i.endswith('.html'):
            continue
        path = os.path.join('html',i)
        print(path)
        d = parseHTML(path)

        for one in d:
            writer.writerow(one)

    out.close()


    print('统计数据量')
    f = open('data.csv')
    data = csv.reader(f)
    c1 = 0
    for i in data:
        c1+=1
    f.close()

    path = 'data_%s.csv'%c1
    shutil.copy('data.csv',path)

    print(c1)
    '''
    pass


def main():
    getAlllink()

    # formatData()
    # countD()
    pass


if __name__ == '__main__':
    main()

