# coding=utf-8
import os
import re
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
import time
from datetime import datetime
import IniFile
# from threa
from pyquery import PyQuery as pq
import LogFile
import mongoDB

class tvoaoSpider(object):
    def __init__(self,driver,log,keyword_list,websearch_url,valid,filter):
        '''

        :param driver: 驱动
        :param log: 日志
        :param keyword_list: 关键字列表
        :param websearch_url: 搜索网址
        :param valid:  采集参数 0：采集当天；1：采集昨天
        :param filter: 过滤项,下面这些内容如果出现在资讯标题中，那么这些内容不要，过滤掉
        '''

        self.log = log
        self.driver = driver
        self.webSearchUrl_list = websearch_url.split(';')
        self.keyword_list = keyword_list
        self.db = mongoDB.mongoDbBase()
        self.valid = valid
        self.start_urls = []
        # 过滤项
        self.filter = filter
        for url in self.webSearchUrl_list:
            self.start_urls.append(url)

    def Comapre_to_days(self,leftdate, rightdate):
        '''
        比较连个字符串日期，左边日期大于右边日期多少天
        :param leftdate: 格式：2017-04-15
        :param rightdate: 格式：2017-04-15
        :return: 天数
        '''
        l_time = time.mktime(time.strptime(leftdate, '%Y-%m-%d'))
        r_time = time.mktime(time.strptime(rightdate, '%Y-%m-%d'))
        result = int(l_time - r_time) / 86400
        return result

    def date_isValid(self, strDateText):
        '''
        判断日期时间字符串是否合法：如果给定时间大于当前时间是合法，或者说当前时间给定的范围内
        :param strDateText: '2017-06-20 10:22 '
        :return: True:合法；False:不合法
        '''
        currentDate = time.strftime('%Y-%m-%d')
        datePattern = re.compile(r'\d{4}-\d{1,2}-\d{1,2}')
        strDate = re.findall(datePattern, strDateText)
        if len(strDate) == 1:
            if self.valid == 0 and self.Comapre_to_days(currentDate, strDate[0]) == 0:
                return True, currentDate
            elif self.valid == 1 and self.Comapre_to_days(currentDate, strDate[0]) == 1:
                return True, str(datetime.datetime.now() - datetime.timedelta(days=1))[0:10]
            elif self.valid == 2 and self.Comapre_to_days(currentDate, strDate[0]) == 2:
                return True, str(datetime.datetime.now() - datetime.timedelta(days=2))[0:10]

        return False, ''


    def log_print(self, msg):
        '''
        #         日志函数
        #         :param msg: 日志信息
        #         :return:
        #         '''
        print('%s: %s' % (time.strftime('%Y-%m-%d %H-%M-%S'), msg))

    def scrapy_date(self):
        try:
            strsplit = '------------------------------------------------------------------------------------'
            for link in self.start_urls:
                try:
                    self.driver.get(link)
                except TimeoutException:
                    self.log.WriteLog('time out after %d seconds when loading page' % 10)
                    self.driver.execute_script('window.stop()')
                    continue

                selenium_html = self.driver.execute_script("return document.documentElement.outerHTML")
                doc = pq(selenium_html)
                infoList = []

                self.log.WriteLog(strsplit)
                self.log_print(strsplit)
                Elements = doc('li[class="content_list clearfix"]')

                for element in Elements.items():
                    date = element('div[class="listtext_label"]').find('span').text().encode('utf8')
                    flag, strDate = self.date_isValid(date)
                    if flag:
                        title = element('div[class="content_listtext"]').find('a').find('h3').text().encode('utf8')
                        if title.find(self.filter)>-1:
                            continue
                        for keyword in self.keyword_list:
                            if title.find(keyword) > -1:
                                url = 'http://www.tvoao.com' + element('a').attr('href')
                                dictM = {'title': title, 'date': strDate,
                                         'url': url, 'keyword': keyword, 'introduction': title, 'source': ''}
                                infoList.append(dictM)
                                break
                if len(infoList) > 0:
                    for item in infoList:
                        item['sourceType'] = 1
                        url = item['url']
                        try:
                            self.driver.get(url)
                        except TimeoutException:
                            self.log.WriteLog('time out after %d seconds when loading page' % 10)
                            self.driver.execute_script('window.stop()')
                            continue
                        htext = self.driver.execute_script("return document.documentElement.outerHTML")
                        dochtml = pq(htext)
                        strSource = dochtml('div[class="headlines_source"]').find('span').eq(1).text().encode(
                            'utf8').replace('\t', '')
                        item['source'] = strSource.replace('\n', '').replace('来源：', '')
                        self.log.WriteLog('title:%s' % item['title'])
                        self.log.WriteLog('url:%s' % item['url'])
                        self.log.WriteLog('date:%s' % item['date'])
                        self.log.WriteLog('source:%s' % item['source'])
                        self.log.WriteLog('kword:%s' % item['keyword'])
                        self.log.WriteLog(strsplit)

                        self.log_print('title:%s' % item['title'])
                        self.log_print('url:%s' % item['url'])
                        self.log_print('date:%s' % item['date'])
                        self.log_print('source:%s' % item['source'])
                        self.log_print('kword:%s' % item['keyword'])
                        self.log_print(strsplit)
                    self.db.SaveInformations(infoList)
        except Exception, e:
            self.log.WriteLog('tvoaoSpider:' + e.message)
        finally:
            pass

#def

# obj = tvoaoSpider()
# obj.scrapy_date()