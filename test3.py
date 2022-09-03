import requests

headers = {
    'authority': 'y.qianzhan.com',
    'pragma': 'no-cache',
    'cache-control': 'no-cache',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="98", "Google Chrome";v="98"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-dest': 'iframe',
    'referer': 'https://y.qianzhan.com/yuanqu/item/7ecc9b257400271d.html',
    'accept-language': 'zh-CN,zh;q=0.9',
    'cookie': 'qznewsite.uid=ufzfuin1z4ophshztq1cbxgl; Hm_lvt_311e89cbd04a90da25b9aebdf23be56d=1662086203; Hm_lpvt_311e89cbd04a90da25b9aebdf23be56d=1662086680',
}

params = (
    ('center', '111.389149,30.661233'),
    ('zoom', '14'),
    ('yid', '7ecc9b257400271d'),
)

response = requests.get('https://y.qianzhan.com/yuanqu/yqmap', headers=headers, params=params)
print(response.text)
#NB. Original query string below. It seems impossible to parse and
#reproduce query strings 100% accurately so the one below is given
#in case the reproduced version is not "correct".
# response = requests.get('https://y.qianzhan.com/yuanqu/yqmap?center=111.389149,30.661233&zoom=14&yid=7ecc9b257400271d', headers=headers)
