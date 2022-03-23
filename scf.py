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
import re
import webbrowser

from selenium import webdriver
import time
import requests
from lxml import etree
import ddddocr
from selenium.webdriver.common.by import By

browser = webdriver.Chrome()
browser.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
    "source": """
    Object.defineProperty(navigator, 'webdriver', {
      get: () => undefined
    })
  """
})

browser.get(
    "https://cg.95306.cn/baseinfor/notice/toBuyNoticeMore?bidType=000&noticeType=01&transactionType=01&navigation=d&wzType=&title=")
# 隐式等待8秒
# browser.implicitly_wait(8)
time.sleep(10)
try:
    browser.find_element(By.XPATH, "//div[@class='next_page']").click()
    time.sleep(10)
    browser.find_element(By.XPATH, "//div[@class='next_page']").click()
    time.sleep(10)
    browser.find_element(By.XPATH, "//div[@class='next_page']").click()
    time.sleep(10)
    browser.find_element(By.XPATH, "//div[@class='next_page']").click()
    time.sleep(20)
except:
    # 截图
    print(browser.page_source)
    "//img[@id='validCodeImg']"
    browser.save_screenshot('./报错网页.png')

    # ddddocr识别验证码
    # repone = etree.HTML(browser.page_source)
    #
    # phones = repone.xpath('//*[@id="validCodeImg"]//@src')
    # phone = 'https://cg.95306.cn'+phones[0]
    # print(phone)
    # derwser = webdriver.Chrome()
    # derwser.get(phone)
    # # 缩放比例  720%
    # derwser.execute_script("document.body.style.zoom='7.2';")
    # derwser.save_screenshot('./验证码.png')
    #
    # ocr = ddddocr.DdddOcr(show_ad=False)
    # with open("./验证码.png", "rb") as f:
    #     img_bytes = f.read()
    # res = ocr.classification(img_bytes)
    # print(res)

    # 人工输入验证码
    res = input('请输入验证码')

    browser.find_element(By.XPATH, "//input[@id='validateCode']").send_keys(res)
    time.sleep(30)
    browser.find_element(By.XPATH, "//a[contains(text(),'确认')]").click()
    time.sleep(2)
    # print()
# browser.close()  # 关闭当前标签页，如果只有一个则关闭浏览器
# browser.quit()  # 彻底关闭，包括后台进程

