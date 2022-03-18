# -*- coding: utf-8 -*-

# @Time : 2022/3/17 9:57
# @Author : 石张毅
# @Site : 
# @File : sele.py
# @Software: PyCharm 
from fake_useragent import UserAgent

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument('--no-sandbox')  # 解决DevToolsActivePort文件不存在的报错
# chrome_options.add_argument("--headless")
chrome_options.headless = True
chrome_options.add_argument('window-size=1400x1015')  # 指定浏览器分辨率
chrome_options.add_argument('--disable-gpu')  # 谷歌文档提到需要加上这个属性来规避bug
chrome_options.add_argument('--hide-scrollbars')  # 隐藏滚动条, 应对一些特殊页面
chrome_options.add_argument('blink-settings=imagesEnabled=false')  # 不加载图片, 提升速度
chrome_options.add_argument('--headless')  # 浏览器不提供可视化页面. linux下如果系统不支持可视化不加这条会启动失败
chrome_options.add_argument('--disable-gpu')  # 禁用GPU加速
chrome_options.add_argument('--start-maximized')  # 浏览器最大化
chrome_options.add_argument('--window-size=1280x1024')  # 设置浏览器分辨率（窗口大小）
chrome_options.add_argument('log-level=3')
chrome_options.add_argument('--disable-infobars')  # 禁用浏览器正在被自动化程序控制的提示
chrome_options.add_argument('--incognito')  # 隐身模式（无痕模式）
chrome_options.add_argument('--disable-javascript')  # 禁用javascript
chrome_options.add_argument('--ignore-certificate-errors')  # 禁用扩展插件并实现窗口最大化
chrome_options.add_argument('–disable-software-rasterizer')
chrome_options.add_argument('--disable-extensions')
chrome_options.add_argument(f'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit'
                            f'/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36')
chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
chrome_options.add_experimental_option('useAutomationExtension', False)
browser = webdriver.Chrome(options=chrome_options)
browser.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
    "source": """
    Object.defineProperty(navigator, 'webdriver', {
      get: () => undefined
    })
  """
})

browser.get("https://weibo.com/ajax/feed/hottimeline?refresh=2&group_id=102803600094&containerid=102803_ctg1_600094_-_ctg1_600094&extparam=discover%7Cnew_feed&max_id=1&count=10")
# 隐式等待8秒
browser.implicitly_wait(2)
print(browser.page_source)

