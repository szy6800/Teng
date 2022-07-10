info = """accept: */*
accept-encoding: gzip, deflate, br
accept-language: zh-CN,zh;q=0.9
content-length: 0
cookie: Hm_lvt_c99546cf032aaa5a679230de9a95c7db=1657189747; Hm_lvt_9bcbda9cbf86757998a2339a0437208e=1657189748; Hm_lpvt_9bcbda9cbf86757998a2339a0437208e=1657189751; qpfccr=true; no-alert3=true; sessionid=xgpu35vehdj26b2iq778wecvsr8hcfp7; Hm_lpvt_c99546cf032aaa5a679230de9a95c7db=1657189757
origin: https://match.yuanrenxue.com
referer: https://match.yuanrenxue.com/match/3
sec-ch-ua: " Not A;Brand";v="99", "Chromium";v="101", "Google Chrome";v="101"
sec-ch-ua-mobile: ?0
sec-ch-ua-platform: "Windows"
sec-fetch-dest: empty
sec-fetch-mode: cors
sec-fetch-site: same-origin
user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.0.0 Safari/537.36"""

headers = {}
for i in info.split('\n'):
    a = i.split(': ',1)
    headers[a[0]]=a[1]

print(headers)
