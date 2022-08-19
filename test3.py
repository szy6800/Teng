import requests

cookies = {
    '4hP44ZykCTt5S': '5Jqk4uTfMdcm21mdg5zxMeKWfjJwK.e6UwVuKMpIp5VOTIyDDDL24XeK7YE4ALfgFWJOY24nBRSVBlK_eog07kG',
    'JSESSIONID': '3AEC08B416804CA03A0D6FAF40F7AC97.tomcat2',
    '4hP44ZykCTt5T': '1rIX90023QR3yLj43vUb4a53mn44EgPMyveJcFTUyhAmq7NqWIrYmniHbjMRQ8IrFEc6QbNfewLHIAcxUeoWEkivdDe_Nj2T__SaErfmuTqRd7BAHWxHJWNRGaGh4mZkj0vtDmeN3UpGfG5MVNUBeEcuqLmuGK4Mqow2OnsbCOGT0t_aQhpSH9cRD50H91pw9Vba0VZZQt.K2ZmxXTw44Y30bNJMTC5uMoi4avbK6ZtDIGZFGV9DaD6CHz..dqM.owF08.lSX2oHK0pwcVUJ6WpGzrzB2bpEIHHblwZCIvtDuPu5MP45kIX1aidL2dC8hobdBRMZL6PgXlEvyVaPuCJHgYPEX4a2fYiLZbcWiLYVFWDWtYDo0L0J6.jWnSDgm7DL2_eEWGId1cSDFbuGGa',
}

headers = {
    'Connection': 'keep-alive',
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Referer': 'http://www.ccgp-gansu.gov.cn/web/doSearchmxarticlelssj.action?limit=20&start=100',
    'Accept-Language': 'zh-CN,zh;q=0.9',
}

params = (
    ('limit', '20'),
    ('start', '100'),
)

response = requests.post('http://www.ccgp-gansu.gov.cn/web/doSearchmxarticlelssj.action', headers=headers, params=params, cookies=cookies, verify=False)
print(response.text)
#NB. Original query string below. It seems impossible to parse and
#reproduce query strings 100% accurately so the one below is given
#in case the reproduced version is not "correct".
# response = requests.get('http://www.ccgp-gansu.gov.cn/web/doSearchmxarticlelssj.action?limit=20&start=120', headers=headers, cookies=cookies, verify=False)
