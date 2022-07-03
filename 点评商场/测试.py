import requests


shopid = 'l2xBxMtsWIf7CezP'
cateId = '10'
tag = '下午茶'
typ = '1'
url = f'https://mapi.dianping.com/shopping/navipoilist?version=9.0.0&shopid={shopid}&shopIdL={shopid}&cityid=2&cateid={cateId}&tag={tag}&type={typ}'
# url = 'https://mapi.dianping.com/shopping/navipoilist?version=9.0.0&shopid=l2xBxMtsWIf7CezP&shopIdL=l2xBxMtsWIf7CezP&cityid=2&cateid=10&tag=%E5%9B%A2%E8%B4%AD%E4%BC%98%E6%83%A0&type=8'

headers = {
 "Accept": "*/*",
 "Accept-Encoding": "gzip, deflate, br",
 "Accept-Language": "zh-CN,zh;q=0.9",
 "Connection": "keep-alive",
 "Cookie": '_lxsdk_cuid=17d311b3888b7-00a24984c52fa1-b7a1438-384000-17d311b3889c8; _lxsdk=17d311b3888b7-00a24984c52fa1-b7a1438-384000-17d311b3889c8; _hc.v=a1860f43-9deb-625f-ebf5-57290c959b18.1637206408; s_ViewType=10; ctu=d556d8e73a270d3894747b895579b86389799a37d028708b158e4b3c033dd1dc; _dp.ac.v=add6f9a8-2a3c-43c1-b312-9faf4698c54d; aburl=1; Hm_lvt_dbeeb675516927da776beeb1d9802bd4=1649759442,1649818197; Hm_lvt_4c4fc10949f0d691f3a2cc4ca5065397=1650267509; fspop=test; Hm_lvt_602b80cf8079ae6591966cc70a3940e7=1654152108,1654492349,1656297622; _lx_utm=utm_source%3DBaidu%26utm_medium%3Dorganic; cityid=2; default_ab=map%3AA%3A1; m_flash2=1; cy=35; cye=taiyuan; WEBDFPID=6v80429u4w285w16z6v242351858vzxv818y17w42u697958yu143x2x-1656738788161-; pvhistory="6L+U5ZuePjo8L3BhZ2VzL2xpc3QvbGlzdD9tYWxsSWQ9SDEyMzl2djZWSFJBUnI0ZSZjYXRlZ29yeUlkPTcwPjo8MTY1NjY1NDA2MjU2Nl1fWw=="; Hm_lpvt_602b80cf8079ae6591966cc70a3940e7=1656654696; _lxsdk_s=181b8d18840-92a-3a6-f74%7C0%7C6',
 "Host": "mapi.dianping.com",
 "Origin": "https://m.dianping.com",
 "Referer": "https://m.dianping.com/",
 "sec-ch-ua": "\" Not A;Brand\";v=\"99\", \"Chromium\";v=\"96\", \"Google Chrome\";v=\"96\"",
 "sec-ch-ua-mobile": "?1",
 "sec-ch-ua-platform": "\"Android\"",
 "Sec-Fetch-Dest": "empty",
 "Sec-Fetch-Mode": "cors",
 "Sec-Fetch-Site": "same-site",
 "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Mobile Safari/537.36"
}


# response = requests.get(url,headers=headers)
# print(response.text)


u = 'https://m.dianping.com/shop/G2Bw7euqTWwaSlkD&shoptype=10&cityid=4487&shopcategoryid=132'
import re
x = re.search('(.*?)&shoptype=',u).group(1)
print(x)