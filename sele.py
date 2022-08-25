import requests

cookies = {
    'SESSION': 'a591c437-1ecb-4c5e-9fde-8284729ca239',
    '__utma': '61363882.2067619981.1661412359.1661412359.1661412359.1',
    '__utmc': '61363882',
    '__utmz': '61363882.1661412359.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)',
}

headers = {
    'Connection': 'keep-alive',
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="98", "Google Chrome";v="98"',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'X-Requested-With': 'XMLHttpRequest',
    'sec-ch-ua-mobile': '?0',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36',
    'sec-ch-ua-platform': '"Windows"',
    'Origin': 'https://wenshu.court.gov.cn',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Dest': 'empty',
    'Referer': 'https://wenshu.court.gov.cn/website/wenshu/181217BMTKHNT2W0/index.html?pageId=7d1a1b7f58ffab611ba9e5098be72c5e&s8=02',
    'Accept-Language': 'zh-CN,zh;q=0.9',
}

data = {
  'pageId': '7d1a1b7f58ffab611ba9e5098be72c5e',
  's8': '02',
  'sortFields': 's50:desc',
  'ciphertext': '1011001 1100111 1001010 1000011 1110001 1001110 1010100 1101110 1000111 1000011 1001011 1101001 1011001 1000100 1111001 1000001 1010111 1001010 1001110 1100110 1011001 1100010 1110001 1110000 110010 110000 110010 110010 110000 111000 110010 110101 110110 1110100 1001000 110010 1101100 1111001 1000100 1111001 1111001 1101010 1100110 101011 1101111 1000110 110110 1101001 1011000 1100110 1100101 1100001 1100101 1000001 111101 111101',
  'pageNum': '2',
  'pageSize': '5',
  'queryCondition': '[{"key":"s8","value":"02"}]',
  'cfg': 'com.lawyee.judge.dc.parse.dto.SearchDataDsoDTO@queryDoc',
  '__RequestVerificationToken': 'mOE314TDDjpNi1b6cBlmyVDe',
  'wh': '649',
  'ww': '1280',
  'cs': '0'
}

response = requests.post('https://wenshu.court.gov.cn/website/parse/rest.q4w', headers=headers, cookies=cookies, data=data)
