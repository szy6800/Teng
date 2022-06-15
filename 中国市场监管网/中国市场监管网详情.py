#-*-coding:utf-8-*-
import re
import json
import requests
from Crypto.Cipher import AES
from 中国市场监管网.tools.jianguan_tools import *
from 中国市场监管网.tools.re_time import Times

tim = Times()

# with open('列表.txt', 'rb') as f:
#     countent = f.read().decode()
#     countent = re.findall(r'"ID":(.*?),',countent)
#     # countent = countent.replace('null', '"null"').replace('true', '"true"')
#     # countent = re.search('"searchResultRecord":(.*?),"ssId"', countent).group(1)
# f.close()
# print(countent)



header = {
 "Accept": "application/json, text/plain, */*",
 "Accept-Encoding": "gzip, deflate",
 "Accept-Language": "zh-CN,zh;q=0.9",
 "accessToken": "jkFXxgu9TcpocIyCKmJ+tfpxe/45B9dbWMUXhdY7vLW6HC3P60H2SFZVgkN1uLDVhpUUKvcMtoMqfGfwdLCb8g==",
 "Cookie": "Hm_lvt_b1b4b9ea61b6f1627192160766a9c55c=1652753863,1652757583; Hm_lpvt_b1b4b9ea61b6f1627192160766a9c55c=1652779660",
 "Host": "jzsc.mohurd.gov.cn",
 "Proxy-Connection": "keep-alive",
 "Referer": "http://jzsc.mohurd.gov.cn/data/project/detail?id=2455454",
 "timeout": "30000",
 "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36"
}



def get_data(url):
    #返回获取到的加密数据
    response = requests.get(url, headers=header)
    if "服务器繁忙，请稍后重试" in response.text:
        return '403'
    # print(response.text)
    return response.text


def _pkcs7unpadding(text):
    """
    处理使用PKCS7填充过的数据
    :param text: 解密后的字符串
    :return:
    """
    length = len(text)#字符长度
    unpadding = ord(text[length - 1])#最后一个字符的ASCII
    #print(text[length - 1])#
    text = text[0:length - unpadding]#切片

    data = text.replace('null', '"null"').replace('true', '"true"')
    result = json.loads(data)["data"]  # str转json数据，获取键值

    return text#整理打印

def parse_data(content):
    """
    AES解密，模式cbc，去填充pkcs7
    :param content: 16进制编码的加密字符串
    :return: 返回解密后的字符串
    """
    iv = '0123456789ABCDEF'#偏移量
    key = 'jo8j9wGw%6HbxfFn'#密钥

    key = bytes(key, encoding='utf-8')
    iv = bytes(iv, encoding='utf-8')

    cipher = AES.new(key, AES.MODE_CBC, iv)#创建一个AES对象（密钥，模式，偏移量）
    decrypt_bytes = cipher.decrypt(bytes.fromhex(content))#解密
    result = str(decrypt_bytes, encoding='utf-8')#编码转换

    length = len(result)  # 字符长度
    unpadding = ord(result[length - 1])  # 最后一个字符的ASCII
    # print(text[length - 1])#
    text = result[0:length - unpadding]  # 切片

    data = text.replace('null', '"null"').replace('true', '"true"')

    result = json.loads(data)["data"]  # str转json数据，获取键值
    return result

def SortData(data):
    data = data.replace('null','"null"').replace('true','"true"')
    result = json.loads(data)["data"]#str转json数据，获取键值
    # for i in result:#循环打印
    #     print(i["QY_ORG_CODE"]+'\t'+
    #           i['QY_NAME']+'\t'+
    #           i['QY_FR_NAME']+'\t'+
    #           i['QY_REGION_NAME']
    #           )



def main(url):
    data = get_data(url)#获取加密数据
    if data == '403':
        return '403'
    zhishi_list = []
    count = parse_data(data)#加密数据解析
    print(count)

    # print(type(count))
    countents = count['list']
    if list == []:
        return '404'
    for i in countents:
        with open('中国市场.txt', 'a+') as f:
            f.write(str(i["ID"])+'\n')
        f.close()



if __name__ == '__main__':
    # 加密数据指向网页
    countent = {'610331': '陕西省-宝鸡市-太白县'}

    print(len(countent))
    total = 0
    for k,v in countent.items():
        for i in range(0,60):
            url = f'http://jzsc.mohurd.gov.cn/api/webApi/dataservice/query/project/list?projectRegionId={k}&pg={str(i)}&pgsz=15&total={str(total)}'
            total += 15
            print(v+f">>>第{str(i+1)}页>>>已出完")
            tf = main(url)
            time.sleep(1)

