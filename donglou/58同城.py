import hashlib
import time

import requests

ti = time.time()
def md5_encrypt(chart):
    md = hashlib.md5(chart.encode())
    return md.hexdigest()
md = 'dfc15b69d3e49e572332b0382d3a0235'
print(md5_encrypt(md))

# new_url = 'https://miniapp.58.com/community/list?cid=1&from=tongcheng_weapp&app=a-wb&platform=windows&b=microsoft&s=Windows10x64&t=1640080116&cv=5.0&wcv=5.0&wv=3.4.5&sv=2.19.2&batteryLevel=0&muid=dfc15b69d3e49e572332b0382d3a0235&weapp_version=1.0.0&user_id=&oid=59C0DD24057E0DEA7C65DBDBA465E3F090973F356CC1FC443F701DE699B5DA8C&udid=59C0DD24057E0DEA7C65DBDBA465E3F090973F356CC1FC443F701DE699B5DA8C&lat=39.9219&lng=116.44355&page=1&page_size=25&city_id=483'
new_url = 'https://miniapp.58.com/community/list?cid=1&from=tongcheng_weapp&app=a-wb&platform=windows&b=microsoft&s=Windows10x64&t=1640081243&cv=5.0&wcv=5.0&wv=3.4.5&sv=2.19.2&batteryLevel=0&muid=dfc15b69d3e49e572332b0382d3a0235&weapp_version=1.0.0&user_id=&oid=59C0DD24057E0DEA7C65DBDBA465E3F090973F356CC1FC443F701DE699B5DA8C&udid=59C0DD24057E0DEA7C65DBDBA465E3F090973F356CC1FC443F701DE699B5DA8C&lat=39.9219&lng=116.44355&page=5&page_size=25&city_id=483'
# new_url = 'https://fa.kaoputou.com/api/region/base-info?region=%E4%B8%8A%E6%B5%B7%E5%B8%82'

header = {
 "Host": "miniapp.58.com",
 "Connection": "keep-alive",
 "Cookie": "aQQ_ajkguid=59C0DD24057E0DEA7C65DBDBA465E3F090973F356CC1FC443F701DE699B5DA8C;PPU=;",
 "PPU": "",
 "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36 MicroMessenger/7.0.9.501 NetType/WIFI MiniProgramEnv/Windows WindowsWechat",
 "X-Forwarded-For": "112.64.131.100",
 "X-WECHAT-HOSTSIGN": "{\"noncestr\"\"a770d0ce9da1845ff3c7185a741997f0\",\"timestamp\"1640080091,\"signature\"\"03350d170415b9b713f7ae8dc138c8f510429710\"}",
 "X_AJK_APP": "a-weapp",
 "ak": "931d0f0a7f7bc73c7cee04b87a1f3cb83d175517",
 "content-type": "application/x-www-form-urlencoded",
 "ft": "ajk-weapp",
 # "sig": "4ad807db76e5110b97acf552c205548f",
 "sig": "68fc39f70f5018cffd531829727ce05d",
 "Referer": "https://servicewechat.com/wxc97b21c63d084d92/193/page-frame.html",
 "Accept-Encoding": "gzip, deflate, br"
}

item = []
response = requests.get(new_url, headers=header)
coun = '甘肃省|'+response.text
# item.append(coun)
# time.sleep(3)
print(coun)


def get_daili(num=1, sheng='', port='1', time1=1):
 # time:1 5-25min 2 25min-3h 3 3-6h 4 6-12h
 # port IP协议 1:HTTP 2:SOCK5 11:HTTPS
 # mr 去重选择（1:360天去重 2:单日去重 3:不去重）
 while 1:
  try:
   url = 'http://webapi.http.zhimacangku.com/getip?num=%s' % num + (
           '&type=1&pro=%s' % sheng + '&city=0&yys=100026&port=%s&time=%s' % (port, time1)) + (
          '&ts=0&ys=0&cs=0&lb=1&sb=0&pb=4&mr=2&regions=')
   s1 = requests.Session()
   s1.mount('https://', HTTPAdapter(max_retries=3))
   content = s1.get(url, timeout=2).text
   ip_list = content.split('\r\n')[0:-1]
   ip_list2 = []
   for ip in ip_list:
    ip_list2.append(ip)
   #                 ip_list2.append({'https':ip,'http':ip})

   print('代理IP:', ip_list2)
   time.sleep(1.2)
   break
  except Exception as e:
   time.sleep(2)
   print(e)
   continue

 return ip_list2


import time
from requests.adapters import HTTPAdapter
import requests

daili = get_daili(time1=2, num=10)
print(daili)


# def get_daili(num=1, sheng='', port='1', time1=1, pack='221123'):
#  # time:1 5-25min 2 25min-3h 3 3-6h 4 6-12h
#  # port IP协议 1:HTTP 2:SOCK5 11:HTTPS
#  # mr 去重选择（1:360天去重 2:单日去重 3:不去重）
#  # pack=221123
#  while 1:
#   try:
#    url = 'http://webapi.http.zhimacangku.com/getip?num=%s' % num + (
#            '&type=1&pro=%s' % sheng + '&city=0&yys=100026&port=%s&time=%s' % (port, time1)) + (
#                  '&ts=0&ys=0&cs=0&lb=1&sb=0&pb=4&mr=2&regions=&pack=%s' % pack)
#    s1 = requests.Session()
#    s1.mount('https://', HTTPAdapter(max_retries=3))
#    content = s1.get(url, timeout=2).text
#    ip_list = content.split('\r\n')[0:-1]
#    ip_list2 = []
#    for ip in ip_list:
#     ip_list2.append(ip)
#     # ip_list2.append({'https': ip, 'http': ip})
#    print('代理IP:', ip_list2)
#    time.sleep(1.2)
#    break
#   except Exception as e:
#    time.sleep(2)
#    print(e)
#    continue
#
#  return ip_list2
#
# daili = get_daili(time1=1, num=20)
# print(daili)


