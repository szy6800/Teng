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

a = "http://ec.ccccltd.cn/PMS/moredetail.shtml?id=sjN7r9ttBwLI2dpg4DQpQb68XreXjaqkS2JQxUxuL5i10fZTCLCagXX5B/CCLxrNujM2HfHDFD2o\r\nZyNybgtLTomDvHhKUmXmKWT7S/uP94uoZyNybgtLTrC6c+4EPKbbV1RQqKvZRNpWRFxeAJJDCVtX\r\nDy8n/F1o"
b = a.replace('\r','').replace('\n','')
print(b)
