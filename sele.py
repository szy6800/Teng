import requests

headers = {
    'authority': 'www.python-spider.com',
    'pragma': 'no-cache',
    'cache-control': 'no-cache',
    'sec-ch-ua': '^\\^',
    'accept': 'application/json, text/javascript, */*; q=0.01',
    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'x-requested-with': 'XMLHttpRequest',
    'sec-ch-ua-mobile': '?0',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36',
    'sec-ch-ua-platform': '^\\^Windows^\\^',
    'origin': 'https://www.python-spider.com',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'referer': 'https://www.python-spider.com/challenge/60',
    'accept-language': 'zh-CN,zh;q=0.9',
    'cookie': 'Hm_lvt_337e99a01a907a08d00bed4a1a52e35d=1658902002,1658975622,1659059953,1659237674; no-alert=true; sessionid=zgz8r8uklpja8ln22erqea13td8llkss; Hm_lpvt_337e99a01a907a08d00bed4a1a52e35d=1659237814',
}

data = {
  'page': '19'
}

response = requests.post('https://www.python-spider.com/api/challenge60/MiiqC+opGnU=', headers=headers, data=data)
print(response.text)