# -*- coding:utf-8 -*-

import requests
import json
import execjs


def fanyis():
    kw = input('请输入你要翻译的文字：')
    url = "https://fanyi.baidu.com/v2transapi?from=zh&to=en"
    headers = {
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Content-Length": "133",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Host": "fanyi.baidu.com",
        "Origin": "https://fanyi.baidu.com",
        "Pragma": "no-cache",
        "Referer": "https://fanyi.baidu.com/translate?aldtype=16047&query=&keyfrom=baidu&smartresult=dict&lang=auto2zh",
        "sec-ch-ua-mobile": "?0",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest",
        'Cookie': 'BIDUPSID=873179ABD1535CB573252A63B8CCB3E5; PSTM=1646391499; REALTIME_TRANS_SWITCH=1; FANYI_WORD_SWITCH=1; SOUND_SPD_SWITCH=1; HISTORY_SWITCH=1; SOUND_PREFER_SWITCH=1; APPGUIDE_10_0_2=1; BDUSS=GV6LUpidlFDeG9mM3dFRjJtWnBzUDRFVTA0d2xCeXZ6b3hlRVVNeTd0a0ZncVJpRVFBQUFBJCQAAAAAAAAAAAEAAAAf9ZmZc2hpMTE5ODUAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAX1fGIF9Xxib; BDUSS_BFESS=GV6LUpidlFDeG9mM3dFRjJtWnBzUDRFVTA0d2xCeXZ6b3hlRVVNeTd0a0ZncVJpRVFBQUFBJCQAAAAAAAAAAAEAAAAf9ZmZc2hpMTE5ODUAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAX1fGIF9Xxib; BAIDUID=BA6D65E1C4453BE33C0F53F336459D54:FG=1; newlogin=1; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; MCITY=-367%3A131%3A; ZFY=UFJHJOiZyAGfUzSaixgRpfIvR1h3TAR7:BEkX90o:Amg8:C; BAIDUID_BFESS=816F7133848C69414CB2FD9DD897904F:FG=1; BDRCVFR[feWj1Vr5u3D]=I67x6TjHwwYf0; delPer=0; PSINO=2; Hm_lvt_64ecd82404c51e03dc91cb9e8c025574=1658889202,1659151491,1659332151,1660099731; BA_HECTOR=2k858kah0la00k8ha0am2m9t1hf69bo17; H_PS_PSSID=36557_36462_36641_36723_36413_37139_36955_36949_36165_36917_36805_36746_37136_26350_36863_36937; RT="z=1&dm=baidu.com&si=6udy2kibaek&ss=l6n6dbdm&sl=8&tt=5nu&bcn=https%3A%2F%2Ffclog.baidu.com%2Flog%2Fweirwood%3Ftype%3Dperf&ul=1gq2f&hd=1gw94"; Hm_lpvt_64ecd82404c51e03dc91cb9e8c025574=1660112236; ab_sr=1.0.1_Nzg1YjNiMWIwMzIwZjg4MDEzMGFhY2FmY2Y0OWU4NmY4YmQ3ZDY2NzQ0ZDIyOGQ2ZDAyMTA2NTU4OGFiZWY3YTg2ZjI3ZmVlZjc1YWZmMzBlYmI0MGEzM2I5YTRjMmI2YjgxZWQ4NTJlZjA4OGUwNzQyNTVkYzcxZmIzNDIyOTY0ZDM1MjYxMjQ5ZmFiYTE4ODQ4MmZkMWQ4MDIyNzc5NWFjOWVhYmI2N2NiMjIzZjVhYzk2ZDFjNGEzOTVlNmJh',
        'Acs-Token': '1660028410583_1660112241245_ALOctco9+mc0VMnvv5LGePns6PeuuBr7y9JznLQgoqFVJAlU5/+QBXeUut0nBgm7qOabbRSJWDP5BsEwaJva1cwtE6TCPemEPiJfCRkZYZ7YDPHeTaSirEdcACMXGUQeE+AHkt2ixQDQVDOOK4d8Dn0nHs5O9pS1OaELiAnIBSiAceXHOk//eQH/laX2TqZP/EDvyz6NrLaINp+iGpqttjZuCHXIrmo4V2Dt3Loui3MNVY7h0CYIkCzjMe7gcUV52uVx9yaZScMp/tx7rOnSAPGCBgnnMN7iJDND2gXoJwGJjXH5/hFuebJBzG4TLjHoUqtUYyGS5ojV734xDUH8Xfxxko4xz1kc/VMZ8DLQkYNHIwqCU+WT1vK7THKoI3nocI3m6fTcEWJfzwb+Nn9qlg=='

    }
    data = {
        'from': 'zh',
        'to': 'en',
        'query': kw,
        'transtype': 'realtime',
        'simple_means_flag': '3',
        'sign': get_baidu_sign(kw),
        'token': 'bbf082ae230a62bb0cd975d3ccaca818',
        'domain': 'common',
    }
    response = requests.post(url, data=data, headers=headers)
    jsondata = json.loads(response.text)['trans_result']['data'][0]['dst']
    print(jsondata)


def get_baidu_sign(kw):
    with open("temp.js") as f:
        jsData = f.read()
        sign = execjs.compile(jsData).call("e", kw)
        return sign


if __name__ == '__main__':
    fanyis()