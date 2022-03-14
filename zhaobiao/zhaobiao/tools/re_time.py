# -*- coding: utf-8 -*-
# @Time    : 2019/7/18 16:46
# @Author  : admin
# @Software: PyCharm
import datetime
import time
import os
import re
from dateutil.relativedelta import relativedelta
from dateutil import parser


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

    def datetimes(self, data):

        if re.match("\s*(\d+)月(\d+)日\s+(\d+)[:：]+(\d+)\s*", data):  # 01月03日 11:16
            dt = self.Datatimes(datetime.datetime.strptime(data, "%m月%d日 %H:%M"), \
                                datetime.date.today().year - 1900)

        if re.match("\s*(\d+)-(\d+)\s+(\d+)[:：]+(\d+)\s*", data):  # 01-03 11:16
            dt = self.Datatimes(datetime.datetime.strptime(data, "%m-%d %H:%M"),
                                datetime.date.today().year - 1900)

        elif re.match("\s*(\d+)年(\d+)月(\d+)日\s+在\s+(\d+)[:：]+(\d+)\s*", data):   #  2020年05月21日 在 11:56
            s = int(Times().seconds)
            str_dt = datetime.datetime.strptime(data, "%Y年%m月%d日 在 %H:%M")
            dt = str_dt + datetime.timedelta(seconds=s)

        # 'Thu Jun 13 12:59:04 +0800 2019'
        elif re.match('(([A-Za-z]+)\s*([A-Za-z]+)\s*(\d+)\s*(\d+)[:：]+(\d+)[:：]+(\d+).*\s*(\d{4}))', data):
            dt = datetime.datetime.strptime(data, '%a %b %d %H:%M:%S +0800 %Y')

        elif re.match("\s*(\d+)-(\d+)-(\d+)$", data):  # 2018-12-17
            datas = '{0} {1}:{2}:{3}'.format(data, Times().hours, Times().minutes, Times().seconds)
            dt = datetime.datetime.strptime(datas, "%Y-%m-%d %H:%M:%S")

        # 2020年05月22日
        elif re.match("\s*(\d+)年(\d+)月(\d+)日\s*", data):
            datas = '{0} {1}:{2}:{3}'.format(data, Times().hours, Times().minutes, Times().seconds)
            times = datetime.datetime.strptime(datas, "%Y年%m月%d日 %H:%M:%S")
            year_add = datetime.date.today().year - 2020
            dt = times + relativedelta(months=12 * year_add)

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

        # '1592260500132'
        elif re.match("\s*(\d{13})", data):
            z = time.localtime(int(int(data) / 1000))
            otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", z)
            dt = datetime.datetime.strptime(otherStyleTime, '%Y-%m-%d %H:%M:%S')

        # '1592260500'
        elif re.match("\s*(\d{10})", data):
            z = time.localtime(int(data))
            otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", z)
            dt = datetime.datetime.strptime(otherStyleTime, '%Y-%m-%d %H:%M:%S')

        # '下午10:53 - 2009年1月24日'
        elif re.match('下午(\d+):(\d+)\s-\s(\d{4}年\d{1,2}月\d{1,2}日)', data):
            s = int(Times().seconds)
            str_dt = datetime.datetime.strptime(data, "下午%H:%M - %Y年%m月%d日")
            dt = str_dt + datetime.timedelta(hours=12) + datetime.timedelta(seconds=s)

        elif re.match("下午\s*(\d+):(\d+)", data):  # 下午 09:13
            days = datetime.date.today() - datetime.date(1900, 1, 1)
            dt = datetime.datetime.strptime(data, "下午 %H:%M") + datetime.timedelta(days=days.days) + datetime.timedelta(hours=12)

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

        # 昨天
        elif re.match('昨天', data):
            time_1 = datetime.date.today() - datetime.timedelta(days=1)
            datas = '{0} {1}:{2}:{3}'.format(time_1, Times().hours, Times().minutes, Times().seconds)
            dt = datetime.datetime.strptime(datas, "%Y-%m-%d %H:%M:%S")

        # 前天 11:12
        elif re.match('前天\s*(\d+):(\d+)', data):
            re_match = re.match('前天\s*(\d+[:：]\d+)', data)
            dt = datetime.datetime.today() - datetime.timedelta(days=2)
            str_dt = dt.strftime("%Y-%m-%d")
            str_dt = '{0} {1}:{2}'.format(str_dt, re_match.group(1), Times().seconds)
            # print(str_dt)
            dt = datetime.datetime.strptime(str_dt, "%Y-%m-%d %H:%M:%S")
            # print(dt)

        # 前天
        elif re.match('前天', data):
            time_1 = datetime.date.today() - datetime.timedelta(days=2)
            datas = '{0} {1}:{2}:{3}'.format(time_1, Times().hours, Times().minutes, Times().seconds)
            dt = datetime.datetime.strptime(datas, "%Y-%m-%d %H:%M:%S")

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
            # 1小时前
        elif re.search("(\d+)小时前", data):
            hours = int(re.search("(\d+)小时前", data).group(1))
            dt = datetime.datetime.now() - datetime.timedelta(hours=hours)
            str_dt = dt.strftime("%Y-%m-%d %H:%M:%S")
            dt = datetime.datetime.strptime(str_dt, "%Y-%m-%d %H:%M:%S")
            # 2天前
        elif re.search("(\d+)天前", data):
            days = int(re.search("(\d+)天前", data).group(1))
            dt = datetime.datetime.now() - datetime.timedelta(days=days)
            str_dt = dt.strftime("%Y-%m-%d %H:%M:%S")
            dt = datetime.datetime.strptime(str_dt, "%Y-%m-%d %H:%M:%S")
            # 1周前
        elif re.search("(\d+)周前", data):
            days = int(re.search("(\d+)周前", data).group(1))
            dt = datetime.datetime.now() - datetime.timedelta(days=-7*days)
            str_dt = dt.strftime("%Y-%m-%d %H:%M:%S")
            dt = datetime.datetime.strptime(str_dt, "%Y-%m-%d %H:%M:%S")

        elif re.match("上午\s*(\d+):(\d+)", data):  # 上午 09:13
            days = datetime.date.today() - datetime.date(1900, 1, 1)
            dt = datetime.datetime.strptime(data, "上午 %H:%M") + datetime.timedelta(days=days.days)


        elif re.match("今天\s*(\d+):(\d+)", data):  # 今天 15:42
            days = datetime.date.today() - datetime.date(1900, 1, 1)
            dt = datetime.datetime.strptime(data, "今天 %H:%M") + datetime.timedelta(days=days.days)

        elif re.match("\s*(\d+)-(\d+)-(\d+)\s+(\d+):(\d+):(\d+)\s*", data):  # 2013-11-11 13:52:35
            try:
                dt = datetime.datetime.strptime(data, "%Y-%m-%d %H:%M:%S")
            except:
                dt = datetime.datetime.strptime(data, "%y-%m-%d %H:%M:%S")

        elif re.match("\s*(\d+)/(\d+)/(\d+)\s+(\d+):(\d+):(\d+)\s*", data):  # 2020/5/1 18:46:33
            try:
                # print(data)
                a = data.replace('/', '-').strip('')[:-8]
                # print(a)
                b = a.split('-')
                for i in range(2):
                    b[1] = b[1].zfill(2)  # 左填充
                    b[2] = b[2].zfill(2)
                # print(b)
                data = '-'.join(b) + data.replace('/', '-').strip('')[-8:]
                # print(data)
                dt = datetime.datetime.strptime(data, "%Y-%m-%d %H:%M:%S")
            except:
                # print(data)
                a = data.replace('/', '-').strip('')[:-8]
                # print(a)
                b = a.split('-')
                for i in range(2):
                    b[1] = b[1].zfill(2)  # 左填充
                    b[2] = b[2].zfill(2)
                # print(b)
                data = '-'.join(b) + data.replace('/', '-').strip('')[-8:]
                # print(data)
                dt = datetime.datetime.strptime(data, "%y-%m-%d %H:%M:%S")

        elif re.match("\s*(\d+)-(\d+)-(\d+)\s+(\d+):(\d+)\s*", data):  # 2013-11-11 13:52
            try:
                dt = datetime.datetime.strptime(data, "%Y-%m-%d %H:%M")
            except:
                dt = datetime.datetime.strptime(data, "%y-%m-%d %H:%M")

        elif re.match("\s*(\d+)/(\d+)/(\d+)\s+(\d+):(\d+)\s*", data):  # 2013/11/11 13:52
            dt = datetime.datetime.strptime(data, "%Y/%m/%d %H:%M")


        else:
            try:
                dt = parser.parse(data)
            except Exception as e:
                print("错误，datetime，没有解析成功, 匹配内容:{} ".format(data),e)
                dt = datetime.datetime.strptime(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),'%Y-%m-%d %H:%M:%S')

        # utc_dt = dt - datetime.timedelta(seconds=28800)
        # 注意此事返回的是datetime.datetime类型的数据
        # 直接使用会出错,建议在导出时对数据进行str()类型转换
        utc_dt = dt - datetime.timedelta()
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

    # 根据数据库时间判断近24小时
    # 判断模糊时间时使用
    def time_now(self, database_time, data_time):

        # 数据库时间
        database_times = datetime.datetime.strptime(database_time, "%Y-%m-%d %H:%M:%S").date()
        # 抓取的微博时间
        data_times = datetime.datetime.strptime(data_time, "%Y-%m-%d %H:%M:%S").date()
        # 今天时间
        today = datetime.datetime.today().date()
        # print(type(database_times))
        # print(type(data_times))
        # print(type(today))
        # 如果抓取的微博时间大于等于数据库的时间并且微博时间小于等于今天的时间
        # 只对日期上进行判断
        if data_times >= database_times and data_times <= today:
            return True
        else:
            return False


if __name__ == "__main__":

    t = Times()
    # print(type(t.hours))
    print(t.datetimes('1623917107000'))
    print(type(t.datetimes('1623917107000')))
    # print(t.datetimes('06-23'))
    # print(t.time_now('2019-06-20 02:11:00', '2019-06-20 11:20:00'))
    # print(t.time_is_Recent('2019-06-18 09:50:40'))
    # test_TimedRotatingFileHandler()
    # logging.warning("Error")