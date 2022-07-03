import requests

cookies = {
    'userName': '',
    'Hm_lvt_06dc77eaa473c9272f6495913fda20e3': '1656653394',
    'number': '27401031',
    'Hm_lpvt_06dc77eaa473c9272f6495913fda20e3': '1656663156',
    'SERVERID': 'e407e27b61d24f269a8a850063b31536|1656663168|1656653393',
}

headers = {
    'Connection': 'keep-alive',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36',
    'Content-Type': 'text/plain;charset=UTF-8',
    'Accept': '*/*',
    'Origin': 'http://ggzyjy.baiyin.gov.cn',
    'Referer': 'http://ggzyjy.baiyin.gov.cn/InfoPage/TradeInfomation.aspx?state=1',
    'Accept-Language': 'zh-CN,zh;q=0.9',
}

params = (
    ('_method', 'getTradeDataList'),
    ('_session', 'no'),
)

data = {
    'infoType': '0',
    'curr': '2',
    'keywords' : '',
    'queryStr':'1,2,3,21,22,23,24,5,6,12,13,14,15,16,17,18,19,20,4,7,8,9,11,41,31,44,43,45,711,441,442,443,0,331,332,333,0'
    }

response = requests.post('http://ggzyjy.baiyin.gov.cn/ajax/InfoPage_TradeInfomation,App_Web_tradeinfomation.aspx.3db62916.nnssip8r.ashx', headers=headers, params=params, cookies=cookies, data=data, verify=False)
print(response.text)
#NB. Original query string below. It seems impossible to parse and
#reproduce query strings 100% accurately so the one below is given
#in case the reproduced version is not "correct".
# response = requests.post('http://ggzyjy.baiyin.gov.cn/ajax/InfoPage_TradeInfomation,App_Web_tradeinfomation.aspx.3db62916.nnssip8r.ashx?_method=getTradeDataList&_session=no', headers=headers, cookies=cookies, data=data, verify=False)



