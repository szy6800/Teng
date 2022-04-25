# -*- coding: utf-8 -*-

# @Time : 2022/4/19 21:24
# @Author : 石张毅
# @Site : 
# @File : tre.py
# @Software: PyCharm
import re
from time import sleep
import time
from selenium.webdriver.common.keys import Keys
''' seleinum 隐形等待的包'''
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium import webdriver
import random,datetime
''' 键盘输入包 '''



class GuoTU_crwl:
    #初始化对象
    def __init__(self):
        url = 'https://www.landchina.com/resultNotice'
        self.url=url
        options = webdriver.ChromeOptions()
        ''' 让浏览器不识别被控制 '''
        options.add_experimental_option('excludeSwitches', ['enable-automation'])
        self.browser = webdriver.Chrome(options=options)
        self.wait = WebDriverWait(self.browser,10) #设置隐形等待时间


    def spider(self):
        #打开网页
        sleep(2)
        trs = self.browser.find_elements_by_xpath('//table[@class="table"]/tr[@class="trHover"]')
        next_bot = self.browser.find_element_by_class_name('btn-next')
        try:
            is_next_bot = next_bot.get_attribute('disabled')
        except:
            is_next_bot = False
        for i in range(len(trs[0:3])):
            trs[i].click()
            #切换到详情页获取信息
            self.browser.switch_to.window(self.browser.window_handles[-1])
            title = self.browser.find_element_by_xpath('//div[@class="conTitle"]').text
            print(title)

            #关掉详情页
            self.browser.close()
            # #切换到首页列表
            self.browser.switch_to.window(self.browser.window_handles[0])
            sleep(0.5)

        return next_bot,is_next_bot

    def run(self):
        self.browser.get(self.url)
        while True:
            next_page,is_next = self.spider()
            if is_next:
                break
            next_page.click()



if __name__ == '__main__':
    a = GuoTU_crwl()
    a.run()