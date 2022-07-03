#-*-coding:utf-8-*-
import time
import re
import json
from urllib import parse

import requests
import hashlib
from requests.adapters import HTTPAdapter
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from lxml import etree
import datetime
import pymysql
from sqlalchemy import create_engine
import pymysql
from sqlalchemy.types import *
import numpy as np
import pandas as pd

def login(ip):
    chrome_options = Options()
    # 设置无头界面
    # chrome_options.add_argument('--headless')
    # 禁止加载图片\js
    #     prefs={
    #          'profile.default_content_setting_values': {
    #             'images': 2,
    #              'javascript': 2
    #         }
    #     }
    prefs = {
        'profile.default_content_setting_values': {
            'images': 2,
        }
    }
    chrome_options.add_experimental_option('prefs', prefs)
    # 设置跨域访问
    chrome_options.add_argument("--args --disable-web-security")
    # 搜狗浏览器请求头
    chrome_options.add_argument(
        # 'user-agent="Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.81 Safari/537.36 SE 2.X MetaSr 1.0"')
        'user-agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.124 Safari/537.36"')
    # 开发者模式，防止检测到slenium
    chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])

    chrome_options.add_experimental_option('useAutomationExtension', False)
    # 禁用启用Blink运行时的功能
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    # 隐身模式
    # chrome_options.add_argument('--incognito')
    # 不打印日志信息
    chrome_options.add_argument('log-level=3')


    path = './chromedriver.exe'
    if ip == '':
        browser = webdriver.Chrome(executable_path=path, chrome_options=chrome_options)
    else:
        PROXY = "http://{}".format(ip)
        options = webdriver.ChromeOptions()
        desired_capabilities = options.to_capabilities()
        desired_capabilities['proxy'] = {
            "httpProxy": PROXY,
            "ftpProxy": PROXY,
            "sslProxy": PROXY,
            "noProxy": None,
            "proxyType": "MANUAL",
            "class": "org.openqa.selenium.Proxy",
            "autodetect": False
        }
        browser = webdriver.Chrome(executable_path=path, chrome_options=chrome_options,
                                   desired_capabilities=desired_capabilities)
    # 设置webdriver.navigator
    browser.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"""}
                            )
    browser.execute_script("Object.defineProperties(navigator,{ webdriver:{ get: () => false } })");
    browser.implicitly_wait(10)
    # browser.set_window_size(600,800)

    return browser

def md5_encrypt(chart):
    md = hashlib.md5(chart.encode())
    return md.hexdigest()

def id_map(url):
    id = re.search('shop/(.*)', url).group(1)
    return id

def analysis(d_list, etrr):
    # print(type(d_list))
    try:
        shang = re.search('%7B%22id%22%3A%22lego-widget-shopping-mall-nav-000-000%22%2C%22meta%22%3A%7B%7D%2C%22props%22%3A%7B%22activeIcon%22%3A0%2C%22entryInfoList%22%3A(.*?)%2C%22navipoilist%22', etrr).group(1)
        shangcheng = parse.unquote(shang)
        d_list.append(shangcheng)
    except:
        d_list.append('无')
        print('>>>>>>>>>>>')
        return d_list

    return d_list

def lng_lat(d_list,map):
    lng = re.search('"shopLng":(.*?),"', map).group(1)
    d_list.append(lng)
    lat = re.search('"shopLat":(.*?),"', map).group(1)
    d_list.append(lat)

    return d_list


def reader(query, db='test'):
    sql = query
    count = 0
    df = ''
    while 1:
        count = count + 1
        try:
            engine = create_engine('mysql+pymysql://root:q!dwyyl6:q3L@127.0.0.1:3306/{}?charset=utf8'.format(db))
            df = pd.read_sql(sql, engine)
            engine.dispose()
            break
        except Exception as e:
            print(e)
            time.sleep(1)
            if count > 2:
                input01 = input('无法连接数据库，回车继续！')
                break
            else:
                continue
    return df


def compare_data(df_1, table, county, db):
    select_sql2 = "select id from %s where county='%s' " % (table, county)
    try:
        df_2 = reader(select_sql2, db=db)
    except Exception as e:
        print('目标表不存在:', e)
        return df_1

    if len(df_2) > 0:
        df_2.drop_duplicates(subset=['id'], keep='first', inplace=True)
        df_2.rename(columns={'id': 'idpp'}, inplace=True)

        df_1 = df_1.merge(df_2, how='left', left_on='id', right_on="idpp")
        df_1['idpp'].fillna(value='', inplace=True)
        print('一共%d条' % len(df_1), end=',')
        df_1 = df_1[df_1['idpp'] == '']
        df_1.drop(columns=['idpp'], inplace=True)
        print('对比后保留%d条' % len(df_1), end=',')
    return df_1


def df_to_mysql(df_all, table2, db):
    df_save = df_all
    if len(df_save) >= 0:
        try:
            engine = create_engine('mysql+pymysql://root:q!dwyyl6:q3L@127.0.0.1:3306/{}?charset=utf8'.format(db))
            df_save.to_sql(name=table2,
                           con=engine,
                           if_exists='append', index=False,
                           chunksize=10000)
            print('保存了%d条数据！' % len(df_save))
            engine.dispose()
        except Exception as e:
            df_save.to_csv('./tomysql_error2.csv', index=False)
            print(e)
            input01 = input('写入数据库错误')

            # 抓取之前对比数据库


def dbz(count):
    # now = datetime.datetime.now()
    # otherStyleTime = now.strftime("%Y-%m-%d")

    sql1 = f'''SELECT id,url,link,title,county FROM `dianping2021` WHERE county='{count}';'''
    sql2 = f'''SELECT id,url,link,title,county FROM `dianping2021_pro` WHERE county='{count}';'''
    # print(sql)
    engine = create_engine('mysql+pymysql://root:Lxp.138927!asd@123.126.87.123:3306/crawler2021?charset=utf8')
    engine2 = create_engine('mysql+pymysql://root:q!dwyyl6:q3L@127.0.0.1:3306/test?charset=utf8')
    df = pd.read_sql(sql1, engine)
    df = df.drop_duplicates(subset=['id']) # 默认保留一条重复数据
    # print(df)
    df1 = pd.read_sql(sql2, engine2)
    df1 = df1.drop_duplicates(subset=['id'])  # 默认保留一条重复数据
    engine.dispose()
    engine2.dispose()
    # print(df1)
    db2 = pd.concat([df, df1], axis=0, sort=False, ignore_index=True)
    # print(db2)
    dbz = db2.drop_duplicates(subset=['id'], keep=False)
    # print(dbz)
    print(f'对比保留了{len(dbz)}条')
    dbz = dbz[['id','url', 'link', 'title','county']].values.tolist() # df转列表
    # print(dbz)
    return dbz


