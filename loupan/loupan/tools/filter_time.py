# -*- coding: utf-8 -*-
# @Time    : 2019/7/18 16:46
# @Author  : admin
# @Software: PyCharm
import datetime
import inspect
import loggig
import os
import re
from dateutil.relativedelta import relativedelta
from dateutil import parser

PAth = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "logging")


class Times(object):
    '''
    strftime 是处理datetime类型
    strptime 是处理str类型的数据
    '''

    @property
    def hours(self):
        hours = str(datetime.datetime.now().hour)
        if len(hours) == 1:
            hours = '0' + hours
            return hours
        return hours

    @property
    def minutes(self):
        minutes = str(datetime.datetime.now().minute)
        if len(minutes) == 1:
            minutes = '0' + minutes
            return minutes
        return minutes

    @property
    def seconds(self):
        seconds = str(datetime.datetime.now().second)
        if len(seconds) == 1:
            seconds = '0' + seconds
            return seconds
        return seconds

    def Datatimes(self, times, year_add):
        dt = times + relativedelta(months=12 * year_add)
        return dt

    def datetimes(self, data: str) -> str:

        if data == '':
            raise Exception('时间为空: %s' % data)

        if re.match("\s*(\d+)月(\d+)日\s+(\d+)[:：]+(\d+)\s*", data):  # 01月03日 11:16
            dt = self.Datatimes(datetime.datetime.strptime(data, "%m月%d日 %H:%M"), \
                                datetime.date.today().year - 1900)

        elif re.match("\s*(\d+)-(\d+)\s+(\d+)[:：]+(\d+)\s*", data):  # 01-03 11:16

            dt = self.Datatimes(datetime.datetime.strptime(data, "%m-%d %H:%M"),
                                datetime.date.today().year - 1900)

        # 'Thu Jun 13 12:59:04 +0800 2019'
        elif re.match('(([A-Za-z]+)\s*([A-Za-z]+)\s*(\d+)\s*(\d+)[:：]+(\d+)[:：]+(\d+).*\s*(\d{4}))', data):
            dt = datetime.datetime.strptime(data, '%a %b %d %H:%M:%S +0800 %Y')

        elif re.match("\s*(\d+)-(\d+)-(\d+)$", data):  # 2018-12-17
            datas = '{0} {1}:{2}:{3}'.format(data, Times().hours, Times().minutes, Times().seconds)
            dt = datetime.datetime.strptime(datas, "%Y-%m-%d %H:%M:%S")


        # 01-10
        elif re.match("\s*(\d+)-(\d+)$", data):
            datas = '{0} {1}:{2}:{3}'.format(data, Times().hours, Times().minutes, Times().seconds)
            times = datetime.datetime.strptime(datas, "%m-%d %H:%M:%S")
            year_add = datetime.date.today().year - 1900
            dt = times + relativedelta(months=12 * year_add)

        # '刚刚'
        elif re.match("刚刚", data):
            time_1 = datetime.date.today()
            datas = '{0} {1}:{2}:{3}'.format(time_1, Times().hours, Times().minutes, Times().seconds)
            dt = datetime.datetime.strptime(datas, "%Y-%m-%d %H:%M:%S")

        # '下午10:53 - 2009年1月24日'
        elif re.match('下午(\d+):(\d+)\s-\s(\d{4}年\d{1,2}月\d{1,2}日)', data):
            s = int(Times().seconds)
            str_dt = datetime.datetime.strptime(data, "下午%H:%M - %Y年%m月%d日")
            dt = str_dt + datetime.timedelta(hours=12) + datetime.timedelta(seconds=s)

        # '上午10:53 - 2009年1月24日'
        elif re.match('上午(\d+):(\d+)\s-\s(\d{4}年\d{1,2}月\d{1,2}日)', data):
            s = int(Times().seconds)
            str_dt = datetime.datetime.strptime(data, "上午%H:%M - %Y年%m月%d日")
            dt = str_dt + datetime.timedelta(seconds=s)

        # 昨天 11:12
        elif re.match('昨天\s*(\d+):(\d+)', data):
            re_match = re.match('昨天\s*(\d+[:：]\d+)', data)
            dt = datetime.datetime.today() - datetime.timedelta(days=1)
            str_dt = dt.strftime("%Y-%m-%d")
            str_dt = '{0} {1}:{2}'.format(str_dt, re_match.group(1), Times().seconds)
            # print(str_dt)
            dt = datetime.datetime.strptime(str_dt, "%Y-%m-%d %H:%M:%S")
            # print(dt)

        elif re.search("(\d+)秒前", data):  # 10秒前
            seconds = int(re.findall("(\d+)秒前", data)[0])
            dt = datetime.datetime.now() - datetime.timedelta(seconds=seconds)
            str_dt = dt.strftime("%Y-%m-%d %H:%M:%S")
            dt = datetime.datetime.strptime(str_dt, "%Y-%m-%d %H:%M:%S")

        # 29分钟前
        elif re.search("(\d+)分钟前", data):  # 29分钟前
            minutes = int(re.findall("(\d+)分钟前", data)[0])
            dt = datetime.datetime.now() - datetime.timedelta(seconds=minutes * 60)
            str_dt = dt.strftime("%Y-%m-%d %H:%M:%S")
            dt = datetime.datetime.strptime(str_dt, "%Y-%m-%d %H:%M:%S")

        elif re.search("(\d+) seconds ago", data):  # 29秒前
            seconds = int(re.findall("(\d+) seconds ago", data)[0])
            dt = datetime.datetime.now() - datetime.timedelta(seconds=seconds)
            str_dt = dt.strftime("%Y-%m-%d %H:%M:%S")
            dt = datetime.datetime.strptime(str_dt, "%Y-%m-%d %H:%M:%S")

        # 1小时前
        elif re.search("(\d+)小时前", data):
            hours = int(re.search("(\d+)小时前", data).group(1))
            dt = datetime.datetime.now() - datetime.timedelta(hours=hours)
            str_dt = dt.strftime("%Y-%m-%d %H:%M:%S")
            dt = datetime.datetime.strptime(str_dt, "%Y-%m-%d %H:%M:%S")
        # 小时前 2 hour ago
        elif re.search("(\d+) hours ago|(\d+) hour ago|(\d+) hr ago|(\d+) hrs ago", data):
            hours = re.search("(\d+) hours ago|(\d+) hour ago|(\d+) hr ago|(\d+) hrs ago", data).group(1)
            if hours is None:
                hours = re.search("(\d+) hours ago|(\d+) hour ago|(\d+) hr ago|(\d+) hrs ago", data).group(2)
                if hours is None:
                    hours = re.search("(\d+) hours ago|(\d+) hour ago|(\d+) hr ago|(\d+) hrs ago", data).group(3)
                    if hours is None:
                        hours = re.search("(\d+) hours ago|(\d+) hour ago|(\d+) hr ago|(\d+) hrs ago", data).group(4)
            hours = int(hours)
            dt = datetime.datetime.now() - datetime.timedelta(hours=hours)
            str_dt = dt.strftime("%Y-%m-%d %H:%M:%S")
            dt = datetime.datetime.strptime(str_dt, "%Y-%m-%d %H:%M:%S")

        # 2天前
        elif re.search("(\d+)天前", data):
            days = int(re.search("(\d+)天前", data).group(1))
            dt = datetime.datetime.now() - datetime.timedelta(days=days)
            str_dt = dt.strftime("%Y-%m-%d %H:%M:%S")
            dt = datetime.datetime.strptime(str_dt, "%Y-%m-%d %H:%M:%S")
        # 1周前  1 week ago
        elif re.search("(\d+) week ago|(\d+) weeks ago", data):
            days = re.search("(\d+) week ago|(\d+) weeks ago", data).group(1)
            if days is None:
                days = re.search("(\d+) week ago|(\d+) weeks ago", data).group(2)
            days = int(days)
            dt = datetime.datetime.now() - datetime.timedelta(days=days * 7)
            str_dt = dt.strftime("%Y-%m-%d %H:%M:%S")
            dt = datetime.datetime.strptime(str_dt, "%Y-%m-%d %H:%M:%S")

        # 2 months ago 2月前
        elif re.search("(\d+) months ago|(\d+) month ago", data):
            days = re.search("(\d+) months ago|(\d+) month ago", data).group(1)
            if days is None:
                days = re.search("(\d+) months ago|(\d+) month ago", data).group(2)
            days = int(days)
            dt = datetime.datetime.now() - datetime.timedelta(days=days * 30)
            str_dt = dt.strftime("%Y-%m-%d %H:%M:%S")
            dt = datetime.datetime.strptime(str_dt, "%Y-%m-%d %H:%M:%S")

        # 2天前 2 days ago
        elif re.search("(\d+) days ago|(\d+) day ago", data):
            days = re.search("(\d+) days ago|(\d+) day ago", data).group(1)
            if days is None:
                days = re.search("(\d+) days ago|(\d+) day ago", data).group(2)
            days = int(days)
            dt = datetime.datetime.now() - datetime.timedelta(days=days)
            str_dt = dt.strftime("%Y-%m-%d %H:%M:%S")
            dt = datetime.datetime.strptime(str_dt, "%Y-%m-%d %H:%M:%S")

            # 2分钟前 2 mins ago
        elif re.search("(\d+) mins ago|(\d+) min ago|(\d+) minute ago|(\d+) minutes ago", data):
            minutes = re.search("(\d+) mins ago|(\d+) min ago|(\d+) minute ago|(\d+) minutes ago", data).group(1)
            if minutes is None:
                minutes = re.search("(\d+) mins ago|(\d+) min ago|(\d+) minute ago|(\d+) minutes ago", data).group(2)
                if minutes is None:
                    minutes = re.search("(\d+) mins ago|(\d+) min ago|(\d+) minute ago|(\d+) minutes ago", data).group(
                        3)
                    if minutes is None:
                        minutes = re.search("(\d+) mins ago|(\d+) min ago|(\d+) minute ago|(\d+) minutes ago",
                                            data).group(4)
            minutes = int(minutes)
            dt = datetime.datetime.now() - datetime.timedelta(seconds=minutes * 60)
            str_dt = dt.strftime("%Y-%m-%d %H:%M:%S")
            dt = datetime.datetime.strptime(str_dt, "%Y-%m-%d %H:%M:%S")


        elif re.match("今天\s*(\d+):(\d+)", data):  # 今天 15:42
            days = datetime.date.today() - datetime.date(1900, 1, 1)
            dt = datetime.datetime.strptime(data, "今天 %H:%M") + datetime.timedelta(days=days.days)

        elif re.match("\s*(\d+)-(\d+)-(\d+)\s+(\d+):(\d+):(\d+)\s*", data):  # 2013-11-11 13:52:35
            try:
                dt = datetime.datetime.strptime(data, "%Y-%m-%d %H:%M:%S")
            except:
                dt = datetime.datetime.strptime(data, "%y-%m-%d %H:%M:%S")

        elif re.match("\s*(\d+)-(\d+)-(\d+)\s+(\d+):(\d+)\s*", data):  # 2013-11-11 13:52

            try:
                dt = datetime.datetime.strptime(data, "%Y-%m-%d %H:%M")
            except:
                dt = datetime.datetime.strptime(data, "%y-%m-%d %H:%M")

        elif re.match("\s*(\d+)/(\d+)/(\d+)\s+(\d+):(\d+)\s*", data):  # 2013/11/11 13:52
            dt = datetime.datetime.strptime(data, "%Y/%m/%d %H:%M")

        # Tue 8:16 PM, Apr 21, 2020  带PM的优先匹配 %I:%M  即 6:35 PM  不是06:35 PM
        elif re.findall("(\w{3})\s*(\d{1,2}:\d{1,2})\s*(\w{2}),\s*(\w{3,10})\s*(\d{1,2}),\s*(\d{4})", data):
            res = re.findall("(\w{3})\s*(\d{1,2}:\d{1,2})\s*(\w{2}),\s*(\w{3,10})\s*(\d{1,2}),\s*(\d{4})", data)
            data = ' '.join(list(res[0]))
            try:
                # 简称
                dt = datetime.datetime.strptime(data, '%a %I:%M %p %b %d %Y')
            except:
                # 全称
                try:
                    dt = datetime.datetime.strptime(data, '%a %I:%M %p %B %d %Y')
                except:
                    try:
                        dt = datetime.datetime.strptime(data, '%a %H:%M %p %b %d %Y')
                    except:
                        dt = datetime.datetime.strptime(data, '%a %H:%M %p %B %d %Y')

        # Published 6:29 P.M. MT April 20, 2020
        elif re.findall("\w+\s*(\d{1,2}:\d{1,2})\s*(\w{1}.[Mm].)\s*\w{2}\s*(\w{3,10})\s*(\d{1,2}),\s*(\d{4})", data):
            res = re.findall("\w+\s*(\d{1,2}:\d{1,2})\s*(\w{1}.[Mm].)\s*\w{2}\s*(\w{3,10})\s*(\d{1,2}),\s*(\d{4})",
                             data)
            data = ' '.join(list(res[0]))
            # print(data)
            data = data.replace('.M.', 'M')
            data = data.replace('a.m.', 'AM')
            data = data.replace('p.m.', 'PM')
            try:
                # 简称
                dt = datetime.datetime.strptime(data, '%I:%M %p %b %d %Y')
            except:
                # 全称
                try:
                    dt = datetime.datetime.strptime(data, '%I:%M %p %B %d %Y')
                except:
                    try:
                        dt = datetime.datetime.strptime(data, '%H:%M %p %B %d %Y')
                    except:
                        dt = datetime.datetime.strptime(data, '%H:%M %p %b %d %Y')

        # Apr 21, 2020 / 06:15 PM CDT Apr 21, 2020 / 06:17 PM CDT
        elif re.findall("(\w{3,10})\s*(\d{1,2}),\s*(\d{4})\s*/\s*(\d{1,2}:\d{1,2})\s*(\w{2})\s*", data):
            res = re.findall("(\w{3,10})\s*(\d{1,2}),\s*(\d{4})\s*/\s*(\d{1,2}:\d{1,2})\s*(\w{2})\s*", data)
            data = ' '.join(list(res[0]))
            try:
                # 简称
                dt = datetime.datetime.strptime(data, '%b %d %Y %I:%M %p')
            except:
                # 全称
                try:
                    dt = datetime.datetime.strptime(data, '%B %d %Y %I:%M %p')
                except:
                    try:
                        dt = datetime.datetime.strptime(data, '%B %d %Y %H:%M %p')
                    except:
                        dt = datetime.datetime.strptime(data, '%b %d %Y %H:%M %p')

        # 06:45, 20 APR 2020Updated06:57, 20 APR 2020
        elif re.findall('\s*(\d{1,2}:\d{1,2}),\s*(\d{1,2})\s*(\w{3,10})\s*(\d{4})', data):
            res = re.findall('\s*(\d{1,2}:\d{1,2}),\s*(\d{1,2})\s*(\w{3,10})\s*(\d{4})', data)
            data = ' '.join(list(res[0]))
            try:
                # 简称
                dt = datetime.datetime.strptime(data, '%I:%M %d %b %Y')
            except:
                # 全称
                try:
                    dt = datetime.datetime.strptime(data, '%I:%M %d %B %Y')
                except:
                    try:
                        dt = datetime.datetime.strptime(data, '%H:%M %d %B %Y')
                    except:
                        dt = datetime.datetime.strptime(data, '%H:%M %d %b %Y')

        # Posted at 6:54 PM, Apr 21, 2020
        elif re.findall('(\d{1,2}:\d{1,2})\s*(\w{2}),\s*(\w{3,10})\s*(\d{1,2}),\s*(\d{4})', data):
            res = re.findall('(\d{1,2}:\d{1,2})\s*(\w{2}),\s*(\w{3,10})\s*(\d{1,2}),\s*(\d{4})', data)
            data = ' '.join(list(res[0]))
            try:
                # 简称
                dt = datetime.datetime.strptime(data, '%I:%M %p %b %d %Y')
            except:
                # 全称
                try:
                    dt = datetime.datetime.strptime(data, '%I:%M %p %b %d %Y')
                except:
                    try:
                        dt = datetime.datetime.strptime(data, '%H:%M %p %b %d %Y')
                    except:
                        dt = datetime.datetime.strptime(data, '%H:%M %p %b %d %Y')

        # March 13, 2020March 13, 2020
        elif re.findall('(\w{3,10})\s*(\d{1,2}),\s*(\d{4})', data):
            res = re.findall('(\w{3,10})\s*(\d{1,2}),\s*(\d{4})', data)
            data = ' '.join(list(res[0]))
            try:
                # 简称
                dt = datetime.datetime.strptime(data, '%b %d %Y')
            except:
                # 全称
                dt = datetime.datetime.strptime(data, '%B %d %Y')

        # Published 22 April 2020
        elif re.findall('\s*(\d{1,2})\s*(\w{3,10})\s*(\d{4})',data):
            res = re.findall('\s*(\d{1,2})\s*(\w{3,10})\s*(\d{4})',data)
            data = ' '.join(list(res[0]))
            try:
                # 简称
                dt = datetime.datetime.strptime(data, '%d %b %Y')
            except:
                # 全称
                dt = datetime.datetime.strptime(data, '%d %B %Y')

        # Wed, 10 Feb 99 10:10:47 EST
        elif re.findall('(\w{3,10}),\s*(\d{1,2})\s*(\w{3,10})\s*(\d{2,4})\s*(\d{1,2}:\d{1,2}:\d{1,2})',data):
            res = re.findall('(\w{3,10}),\s*(\d{1,2})\s*(\w{3,10})\s*(\d{2,4})\s*(\d{1,2}:\d{1,2}:\d{1,2})',data)
            data = ' '.join(list(res[0]))
            try:
                # 简称
                dt = datetime.datetime.strptime(data, '%a %d %b %y %H:%M:%S')
            except:
                # 全称
                try:
                    dt = datetime.datetime.strptime(data, '%a %d %B %y %H:%M:%S')
                except:
                    try:
                        dt = datetime.datetime.strptime(data, '%a %d %b %Y %H:%M:%S')
                    except:
                        dt = datetime.datetime.strptime(data, '%a %d %B %Y %H:%M:%S')

        # Apr. 23, 2020
        elif re.findall('(\w{3,10})[\s*|.]\s*(\d{1,2})[,|\s*]\s*(\d{4})',data):
            res = re.findall('(\w{3,10})[\s*|.]\s*(\d{1,2})[,|\s*]\s*(\d{4})',data)
            data = ' '.join(list(res[0]))
            try:
                # 简称
                dt = datetime.datetime.strptime(data, '%b %d %Y')
            except:
                # 全称
                dt = datetime.datetime.strptime(data, '%B %d %Y')

        # 입력 : 2020-04-23 16:23
        elif re.findall('(\d{4})[-/.](\d{1,2})[-/.](\d{2})\s*(\d{1,2}:\d{1,2})',data):
            res = re.findall('(\d{4})[-/.](\d{1,2})[-/.](\d{2})\s*(\d{1,2}:\d{1,2})',data)
            data = ' '.join(list(res[0]))
            try:
                # 简称
                dt = datetime.datetime.strptime(data,'%Y %m %d %H:%M')
            except:
                # 全称
                dt = datetime.datetime.strptime(data,'%Y %m %d %I:%M')

        # Posted Fri, April 24th, 2020 9:00 am
        elif re.findall('(\w{3,10})[,|\s*]\s*(\w{3,10})\s*(\d{2})\s*\w{1,3}[,|\s*]\s*(\d{4})\s*(\d{1,2}:\d{1,2})\s*(\w{2})', data):
            res = re.findall('(\w{3,10})[,|\s*]\s*(\w{3,10})\s*(\d{2})\s*\w{1,3}[,|\s*]\s*(\d{4})\s*(\d{1,2}:\d{1,2})\s*(\w{2})', data)
            data = ' '.join(list(res[0]))
            try:
                dt =datetime.datetime.strptime(data,'%a %B %d %Y %I:%M %p')
            except:
                try:
                    dt = datetime.datetime.strptime(data,'%a %B %d %Y %H:%M')
                except:
                    try:
                        dt = datetime.datetime.strptime(data, '%a %b %d %Y %I:%M %p')
                    except:
                        try:
                            dt = datetime.datetime.strptime(data, '%a %b %d %Y %H:%M')
                        except:
                            dt = parser.parse(data)

        # Updated 01/02/2020
        elif re.findall('\s*(\d{1,2})[.-/](\d{1,2})[.-/](\d{2,4})',data):
            res = re.findall('\s*(\d{1,2})[.-/](\d{1,2})[.-/](\d{2,4})',data)
            data = ' '.join(list(res[0]))
            try:
                dt = datetime.datetime.strptime(data,'%m %d %Y')
            except:
                dt = datetime.datetime.strptime(data, '%m %d %y')

        else:
            try:
                dt = datetime.datetime.strptime(data, '%a%b%d%H:%M:%SCST%Y')
            except:
                try:
                    # Fri Mar 13 15:43:59 CST 2020
                    dt = datetime.datetime.strptime(data, '%a %b %d %H:%M:%S CST %Y')
                except:
                    try:
                        dt = parser.parse(data)
                    except Exception as e:
                        print("错误，datetime，没有解析成功, 匹配内容:{} ".format(data))
                        dt = ''
        # utc_dt = dt - datetime.timedelta(seconds=28800)
        utc_dt = dt - datetime.timedelta()
        if isinstance(utc_dt, datetime.datetime):
            utc_dt = utc_dt.strftime("%Y-%m-%d %H:%M:%S")
        return utc_dt

    def datetimes2(self,date_str):
        if isinstance(date_str, datetime.datetime):
            utc_dt = date_str.strftime("%Y-%m-%d")
        else:
            utc_dt = datetime.datetime.strptime(date_str,"%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d")
        return utc_dt


    # 判断是否是近2天的时间
    def time_is_Recent(self, times):
        # 今天时间
        today = datetime.datetime.now().strftime('%Y-%m-%d')
        # 昨天时间 str
        yesterday = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime('%Y-%m-%d')
        # 匹配类似于 2019-04-26 11:07:00
        filter_time = re.compile('(20\d{2}[年|\-|.|/][01]?\d{1}[月|\-|.|/][0123]?\d{1}日?)')
        re_match = re.match(filter_time, times)
        if re_match:
            if re_match.group(1) == today or re_match.group(1) == yesterday:
                return True
            else:
                # print('Time is No Match')
                return False

    # 判断是否是24小时的数据
    def time_is_Recent_2(self, times):
        # 今天时间
        today = datetime.datetime.now().strftime('%Y-%m-%d')
        # 昨天时间 str
        yesterday = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime('%Y-%m-%d')
        # 匹配类似于 2019-04-26 11:07:00
        filter_time = re.compile('(20\d{2}[年|\-|.|/][01]?\d{1}[月|\-|.|/][0123]?\d{1}日?)')
        re_match = re.match(filter_time, times)
        print(re_match.group(1))
        if re_match:
            if re_match.group(1) == today:
                return True
            else:
                # print('Time is No Match')
                return False

    # 判断时间是否有,如果有则按时间判断,没有则返回
    # 判断准确时间时使用
    def time_now_2(self, database_time, data_time):
        # print('-----------开始判断时间-----------')
        # 数据库时间
        database_times = datetime.datetime.strptime(database_time, "%Y-%m-%d %H:%M:%S")
        # 抓取的微博时间
        data_times = datetime.datetime.strptime(data_time, "%Y-%m-%d %H:%M:%S")
        # 当前时间
        now_times = datetime.datetime.now()
        if data_times > database_times and data_times <= now_times:
            return True
        else:
            return False


# 过滤emoji表情
def filter_emoji(desstr, restr=''):
    try:
        co = re.compile(u'[\U00010000-\U0010ffff]')
    except re.error:
        co = re.compile(u'[\uD800-\uDBFF][\uDC00-\uDFFF]')
    return co.sub(restr, desstr)


if __name__ == "__main__":
    t = Times()
    # print(t.datetimes('1591749983000'))
    # print(t.datetimes('Published 6:29 P.M. MT April 20, 2020'))
    # print(t.datetimes('Apr 21, 2020 4 hrs ago'))
    # print(t.datetimes('6 seconds ago'))
    # print(t.datetimes('April 21 2020 - 10:30PM'))
    # print(t.datetimes('Apr 21, 2020 / 11:36 AM CDT'))
    # print(t.datetimes('Apr 21, 2020 / 06:15 PM CDT Apr 21, 2020 / 06:17 PM CDT'))
    # print(t.datetimes('06:45, 20 APR 2020Updated06:57, 20 APR 2020'))
    # print(t.datetimes('Apr 17, 2020'))
    # print(t.datetimes('Apr 3, 2020'))
    # print(t.datetimes('March 13, 2020March 13, 2020'))
    # print(t.datetimes('Apr 21, 2020 / 09:28 PM EDTApr 21, 2020 / 09:28 PM EDT'))
    # print(t.datetimes('1 week ago'))
    # print(t.datetimes('3 weeks ago'))
    # print(t.datetimes('Tue 8:16 PM, Apr 21, 2020'))
    # print(t.datetimes('Posted at 6:54 PM, Apr 21, 2020'))
    # print(t.datetimes('Published 10:15 a.m. ET April 20, 2020'))
    # print(t.datetimes('Published 6:29 P.M. MT April 20, 2020'))
    # print(t.datetimes('2 months ago'))
    # print(t.datetimes('2 day ago'))
    # print(t.datetimes('2 hr ago'))
    # print(t.datetimes('2 hour ago'))
    # print(t.datetimes('2 hours ago'))
    # print(t.datetimes('2 hrs ago'))
    # print(t.datetimes('Published 22 April 2020'))
    # print(t.datetimes('Wed, 10 Feb 99 10:10:47 EST'))
    # print(t.datetimes('Updated 56 min ago'))
    # print(t.datetimes('입력 : 2020-04-23 16:23'))
    # print(t.datetimes('56 minute ago'))
    # print(t.datetimes('Posted Fri, April 24th, 2020 9:00 am'))
    # print(t.datetimes('Fri April 24 2020 9:00 am'))
    # print(t.datetimes('Updated 01/02/2020'))
    # print(t.datetimes('10:37, 20 APR 2020'))
    # print(t.datetimes('May 12, 2020 at 7:17 PM'))

