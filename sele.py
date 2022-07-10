
import requests_html
import time
import json
import base64
import re
import subprocess
from Crypto.Util.Padding import pad, unpad
from Crypto.Cipher import AES, DES
from Crypto.Hash import MD5


def encrypt_data_aes(text, key, iv):
    secretkey = MD5.new(key.encode()).hexdigest()[16:]
    secretiv = MD5.new(iv.encode()).hexdigest()[:16]
    crypto = AES.new(key=secretkey.encode(), mode=AES.MODE_CBC, iv=secretiv.encode())
    return base64.b64encode(crypto.encrypt(pad(text.encode(), AES.block_size))).decode()


def encrypt_data_des(text, key, iv):
    secretkey = MD5.new(key.encode()).hexdigest()[:8]
    secretiv = MD5.new(iv.encode()).hexdigest()[24:]
    crypto = DES.new(key=secretkey.encode(), mode=DES.MODE_CBC, iv=secretiv.encode())
    return base64.b64encode(crypto.encrypt(pad(text.encode(), DES.block_size))).decode()


def decrypt_data(text, data):
    keyid = re.findall('(?<=data = AES\.decrypt\(data, ).+?(?=,)', data)[0]
    key = re.findall('(?<=const )' + keyid + ' = ".+?(?=")', data)[0].split('"')[-1]
    ivid = re.findall('(?<=, )' + keyid + ', .+?(?=\))', data)[0].split(', ')[-1].split(',')[-1]
    iv = re.findall('(?<=const )' + ivid + ' = ".+?(?=")', data)[0].split('"')[-1]
    secretkey = MD5.new(key.encode()).hexdigest()[16:]
    secretiv = MD5.new(iv.encode()).hexdigest()[:16]
    crypto = AES.new(key=secretkey.encode(), mode=AES.MODE_CBC, iv=secretiv.encode())
    text = unpad(crypto.decrypt(base64.b64decode(text.encode())), AES.block_size)
    keyid = re.findall('(?<=data = DES\.decrypt\(data, ).+?(?=,)', data)[0]
    key = re.findall('(?<=const )' + keyid + ' = ".+?(?=")', data)[0].split('"')[-1]
    ivid = re.findall('(?<=, )' + keyid + ', .+?(?=\))', data)[0].split(', ')[-1].split(',')[-1]
    iv = re.findall('(?<=const )' + ivid + ' = ".+?(?=")', data)[0].split('"')[-1]
    secretkey = MD5.new(key.encode()).hexdigest()[:8]
    secretiv = MD5.new(iv.encode()).hexdigest()[24:]
    crypto = DES.new(key=secretkey.encode(), mode=DES.MODE_CBC, iv=secretiv.encode())
    text = unpad(crypto.decrypt(base64.b64decode(text)), DES.block_size)
    return base64.b64decode(text).decode()


def main():
    requests = requests_html.HTMLSession()
    url = 'https://www.aqistudy.cn/html/city_realtime.php?v=2.3'
    headers = {
        'User-Agent': 'Mozilla/5.0(WindowsNT10.0;WOW64)AppleWebKit/537.36(KHTML,likeGecko)Chrome/69.0.3497.100Safari/537.36',
    }
    response = requests.get(url, headers=headers)
    url = filter(lambda n: '/js/encrypt_' in n.attrs['src'], filter(lambda n: 'src' in n.attrs.keys(), response.html.xpath('//script'))).__next__().attrs['src'].replace('../js/', 'https://www.aqistudy.cn/js/')
    print(url)
    response = requests.get(url, headers=headers)
    data = response.text
    while data.startswith("eval("):
        with open('temp.js', 'w', encoding='utf-8') as f:
            f.write('console.log(' + data.strip()[5:-1] + ')')

        nodejs = subprocess.Popen('node temp', stderr=subprocess.PIPE, stdout=subprocess.PIPE)
        data = nodejs.stdout.read().decode().replace('\n', '')

        if 'dswejwehxt(dswejwehxt' in data:
            data = re.findall('(?<=dswejwehxt\(dswejwehxt\().+?(?=\))', data)[0][1:-1]
            data = base64.b64decode(base64.b64decode(data.encode())).decode()
        elif 'dswejwehxt(' in data:
            data = re.findall('(?<=dswejwehxt\().+?(?=\))', data)[0][1:-1]
            data = base64.b64decode(data.encode()).decode()

    # 格式化代码
    with open('temp.js', 'w', encoding='utf-8') as f:
        f.write(data)

    nodejs = subprocess.Popen('node script', stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    data = nodejs.stdout.read().decode()

    appId = re.findall("(?<=var appId = ').+?(?=')", data)[0]
    clienttype = 'WEB'
    timestamp = int(time.time() * 1000)
    method = 'GETDATA'
    objectdata = {
        'city': '杭州'
    }
    param = {
        'appId': appId,
        'method': method,
        'timestamp': timestamp,
        'clienttype': clienttype,
        'object': objectdata,
        'secret': MD5.new((appId + method + str(timestamp) + clienttype + json.dumps(objectdata, ensure_ascii=False, separators=(',', ':'))).encode()).hexdigest()
    }
    print(param)
    param = base64.b64encode(json.dumps(param, ensure_ascii=False, separators=(',', ':')).encode()).decode()
    print(param)
    if 'param = AES.encrypt' in data:
        keyid = re.findall('(?<=param = AES\.encrypt\(param, ).+?(?=,)', data)[0]
        key = re.findall('(?<=const )' + keyid + ' = ".+?(?=")', data)[0].split('"')[-1]
        ivid = re.findall("(?<=, )" + keyid + ', .+?(?=\))', data)[0].split(', ')[-1]
        iv = re.findall('(?<=const )' + ivid + ' = ".+?(?=")', data)[0].split('"')[-1]
        param = encrypt_data_aes(param, key, iv)
    elif 'param = DES.encrypt' in data:
        keyid = re.findall('(?<=param = DES\.encrypt\(param, ).+?(?=,)', data)[0]
        key = re.findall('(?<=const )' + keyid + ' = ".+?(?=")', data)[0].split('"')[-1]
        ivid = re.findall("(?<=, )" + keyid + ', .+?(?=\))', data)[0].split(', ')[-1]
        iv = re.findall('(?<=const )' + ivid + ' = ".+?(?=")', data)[0].split('"')[-1]
        param = encrypt_data_des(param, key, iv)


    dataid = re.findall('(?<=data: \{).+?(?=\})', data, re.S)[0].replace('\n', '').strip().split(':')[0]
    url = 'https://www.aqistudy.cn/apinew/aqistudyapi.php'
    postdata = {
        dataid: param
    }
    response = requests.post(url, headers=headers, data=postdata)
    print(response.text)
    data = decrypt_data(response.text, data)
    print(data)

if __name__ == '__main__':
    main()
