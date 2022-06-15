
# import requests


# def one():
#     url = 'http://i.meituan.com/index/DealList?num=0.46111196686919564'
#     headers = {
#         'Cookie': '__mta=244273466.1652429888384.1652429888384.1652429971303.2; _lxsdk_cuid=180bc6bcc38c8-0987d5f8874b8e-c3f3568-144000-180bc6bcc39c8; lat=39.697924; lng=116.292149; ci=1; cityname=%E5%8C%97%E4%BA%AC; webloc_geo=39.697924%2C116.292149%2Cwgs84%2C-1; ci3=1; JSESSIONID=node0ok0zi3ukbyyux6cmpja40x0k84144479.node0; IJSESSIONID=node0ok0zi3ukbyyux6cmpja40x0k84144479; iuuid=6D920D34E3CFD9F0115FB404844EDCDC227C4E2CECA21E326977E4E6512AFBB9; _lxsdk=6D920D34E3CFD9F0115FB404844EDCDC227C4E2CECA21E326977E4E6512AFBB9; webp=1; __utma=74597006.1694163828.1652429889.1652429889.1652429889.1; __utmc=74597006; __utmz=74597006.1652429889.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); WEBDFPID=502860x7u849523501u05zv0xz6591x4819yx2u61v197958wx02vwvu-1652516296068-1652429894881UOGYYKIfd79fef3d01d5e9aadc18ccd4d0c95071986; uuid=c7b6b368c71d423ca3dd.1652429896.1.0.0; _lx_utm=utm_source%3DBaidu%26utm_medium%3Dorganic; latlng=39.697924,116.292149,1652429975999; __utmb=74597006.5.9.1652429975445; _lxsdk_s=180bc6bcc3b-569-5e0-bf9%7C%7C12; i_extend=H__a100002__b1',
#         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36'
#     }
#     ron = requests.get(url,headers=headers)
#     print(ron.text)
#
# if __name__ == '__main__':
#     one()




import requests
import json

def one():
    url = 'https://api.landchina.com/tGdxm/result/list'
    for i in range(1,601):
        headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9,ga;q=0.8',
            'Connection': 'keep-alive',
            # 'Content-Length': '55',
            'Content-Type': 'application/json',
            'Hash': '142bd26657427947669a76d960e46ca16688ca72f00256e96cb269d4e2ff0b14',
            'Host': 'api.landchina.com',
            'Origin': 'https://www.landchina.com',
            'Referer': 'https://www.landchina.com/',
            'sec-ch-ua': '"Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-site',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36'

       }
        datas = {'pageNum': i, 'pageSize': 10, 'startDate': "", 'endDate': "",'xzqDm': "63"}

        data = json.dumps(datas)
        # print(type(data))
        ron = requests.post(url,headers=headers,data=data,allow_redirects=False)
        print(ron.text)

if __name__ == '__main__':
    one()
