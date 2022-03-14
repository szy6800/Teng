# -*- coding: utf-8 -*-

# @Time : 2022/3/10 18:16
# @Author : 石张毅
# @Site : 
# @File : scf.py
# @Software: PyCharm 
from selenium.webdriver.common.by import By
from selenium import webdriver
import time
from lxml import etree
from selenium.webdriver.chrome.options import Options
import csv
import os
import datetime


# 采集开始时间
def start_time():
    start_times = datetime.datetime.now()  # 采集开始时间
    start_tim = str(start_times).split('.')[0]
    print('采集开始时间 ===>', start_tim)
    return start_tim


# 采集完成用时
def stop_time(start_tim):
    print('采集已完成>>>>>>>>')
    end_time = str(datetime.datetime.now()).split('.')[0]  # 采集结束时间

    print(f"Starting time ===> {start_tim}, End time ===> {end_time}")
    return end_time

# 下载本地html
def html():
    folder_path = './/192_html'
    if not os.path.exists(folder_path):  # 判断是否存在文件夹如果不存在则创建为文件夹
        os.makedirs(folder_path)
    res1 = browser.page_source
    res1 = res1.encode()
    open(f'.//192_html//{tt}.html', 'wb').write(res1)
    print(f'{tt}.html保存成功')


# 遍历搜索
def php():
    browser.find_element(By.XPATH,"//input[@id='peopleBusinesses_name']").send_keys(it)
    time.sleep(5)
    browser.find_element(By.XPATH,"//input[@id='searchBtn']").click()
    time.sleep(5)
    browser.find_element(By.XPATH,"(//input[@id='peopleBusinesses_name'])[1]").clear()
    time.sleep(5)


if __name__ == '__main__':
    start = start_time()
    # 无界面模式
    chrome_options = Options()
    chrome_options.add_argument('--no-sandbox')  # 解决DevToolsActivePort文件不存在的报错
    chrome_options.add_argument('window-size=1920x3000')  # 指定浏览器分辨率
    chrome_options.add_argument('--disable-gpu')  # 谷歌文档提到需要加上这个属性来规避bug
    chrome_options.add_argument('--hide-scrollbars')  # 隐藏滚动条, 应对一些特殊页面
    chrome_options.add_argument('blink-settings=imagesEnabled=false')  # 不加载图片, 提升速度
    chrome_options.add_argument('--headless')  # 浏览器不提供可视化页面. linux下如果系统不支持可视化不加这条会启动失败
    chrome_options.add_argument('--headless')  # 无头模式，可不启用界面显示运行
    chrome_options.add_argument('--disable-gpu')  # 禁用GPU加速
    chrome_options.add_argument('--start-maximized')  # 浏览器最大化
    chrome_options.add_argument('--window-size=1280x1024')  # 设置浏览器分辨率（窗口大小）
    chrome_options.add_argument('log-level=3')
    chrome_options.add_argument('--user-agent=""')  # 设置请求头的User-Agent
    chrome_options.add_argument('--disable-infobars')  # 禁用浏览器正在被自动化程序控制的提示
    chrome_options.add_argument('--incognito')  # 隐身模式（无痕模式）
    chrome_options.add_argument('--hide-scrollbars')  # 隐藏滚动条, 应对一些特殊页面
    chrome_options.add_argument('--disable-javascript')  # 禁用javascript
    chrome_options.add_argument('--blink-settings=imagesEnabled=false')  # 不加载图片, 提升速度
    chrome_options.add_argument('--ignore-certificate-errors')  # 禁用扩展插件并实现窗口最大化
    chrome_options.add_argument('–disable-software-rasterizer')
    chrome_options.add_argument('--disable-extensions')

    browser = webdriver.Chrome(options=chrome_options)
    # browser = webdriver.Chrome()
    browser.get(
        "https://www.192.com/people/search/")
    time.sleep(3)
    browser.find_element(By.XPATH,"//div[@class='ont-btn-main ont-cookies-btn js-ont-btn-ok2']").click()
    time.sleep(5)
    # 遍历名单
    f = open('EnglishNameList.txt', encoding='utf-8')

    for i in f:
        name = i.strip()
        t = name.split(' ', 1)
        if len(t) != 2:
            continue
        it = f'{t[0]} {t[1]}'
        tt = f'{t[0]}_{t[1]}'
        print(it)
        try:
            php()
            html()
        except:
            print('******************************')
            print(f'>>>>>>>>>>>>>>>>={tt}>>报错')

    browser.close() # 关闭当前标签页，如果只有一个则关闭浏览器
    browser.quit()  # 彻底关闭，包括后台进程
    print(stop_time(start))
