import requests

cookies = {
    'userName': '',
    'number': '7813328',
    'Hm_lvt_06dc77eaa473c9272f6495913fda20e3': '1651832576,1651924949',
    'Hm_lpvt_06dc77eaa473c9272f6495913fda20e3': '1651924949',
    'SERVERID': '0b3aa6573e07062bec60dd6a5ba7cc33|1651926330|1651924942',
}

headers = {
    'Connection': 'keep-alive',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36',
    'Content-Type': 'text/plain;charset=UTF-8',
    'Accept': '*/*',
    'Origin': 'http://ggzyjy.baiyin.gov.cn',
    'Referer': 'http://ggzyjy.baiyin.gov.cn/InfoPage/TradeInfomation.aspx?state=1,2,3',
    'Accept-Language': 'zh-CN,zh;q=0.9',
}

params = (
    ('_method', 'getTradeDataList'),
    ('_session', 'no'),
)

data = {
  '$infoType': '0\\r\\ncurr=3\\r\\nkeywords=\\r\\nqueryStr=and  a.PrjPropertyNew in (1,2,3,21,22,23,24,5,6,12,13,14,15,16,17,18,19,20,4,7,8,9,11,41,31,44,43,45,711,441,442,443,0,331,332,333,0) and a.Field1 in(3259,2955,2956,2957,2958,2959,2960)'
}

response = requests.post('http://ggzyjy.baiyin.gov.cn/ajax/InfoPage_TradeInfomation,App_Web_tradeinfomation.aspx.3db62916.arderj2p.ashx', headers=headers, params=params, cookies=cookies, data=data, verify=False)
print(response.text)
#NB. Original query string below. It seems impossible to parse and
#reproduce query strings 100% accurately so the one below is given
#in case the reproduced version is not "correct".
# response = requests.post('http://ggzyjy.baiyin.gov.cn/ajax/InfoPage_TradeInfomation,App_Web_tradeinfomation.aspx.3db62916.arderj2p.ashx?_method=getTradeDataList&_session=no', headers=headers, cookies=cookies, data=data, verify=False)
