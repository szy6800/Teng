# -*- coding: utf-8 -*-
import datetime
import sys
from time import sleep
from selenium import webdriver
# from selenium.common.exceptions import ElementClickInterceptedException, NoSuchElementException
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

# from xlrd import open_workbook
# from xlutils.copy import copy
# from pynput.mouse import Controller, Button, Listener as MouseLister

# chrome_options 初始化选项
sys.setrecursionlimit(1000000)
# chrome_options 初始化选项
chrome_options = webdriver.ChromeOptions()
# 设置浏览器初始 位置x,y & 宽高x,y
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_argument(f'--window-position={217},{92}')
chrome_options.add_argument(f'--window-size={1222},{816}')
chrome_options.add_experimental_option("excludeSwitches", ['enable-automation'])
chrome_options.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})
chrome_options.add_argument('–headless')
desired_capabilities = DesiredCapabilities.CHROME  # 修改页面加载策略
desired_capabilities["pageLoadStrategy"] = "none"
driver = webdriver.Chrome(chrome_options=chrome_options)
with open('stealth.min.js') as f:
    js = f.read()
driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
  "source": js
})
driver.set_page_load_timeout(10)
driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
    "source": """Object.defineProperty(navigator, 'webdriver', {get: () => undefined})""",
})
wait = WebDriverWait(driver, 20)


def main():
    try:
        driver.get('https://www.itjuzi.com/login')
    except:
        driver.execute_script('window.stop()')
    sleep(100)


if __name__ == '__main__':
    main()
