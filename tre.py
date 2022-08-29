"""
全国建筑市场监管公共服务平台，首页信息获取
http://jzsc.mohurd.gov.cn/data/company
"""

import requests

from Cryptodome.Cipher import AES
import json

header = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36",
}


def get_data(url):
    #返回获取到的加密数据
    response = requests.get(url, headers=header)
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

    SortData(text)#整理打印

def parse_data(content):
    """
    AES解密，模式cbc，去填充pkcs7
    :param content: 16进制编码的加密字符串
    :return: 返回解密后的字符串
    """
    iv = '0123456789ABCDEF'#偏移量
    key = 'jo8j9wGw%6HbxfFn'#**

    key = bytes(key, encoding='utf-8')
    iv = bytes(iv, encoding='utf-8')

    cipher = AES.new(key, AES.MODE_CBC, iv)#创建一个AES对象（**，模式，偏移量）
    decrypt_bytes = cipher.decrypt(bytes.fromhex(content))#解密
    result = str(decrypt_bytes, encoding='utf-8')#编码转换

    _pkcs7unpadding(result)#处理填充过的数据

def SortData(data):
    result = json.loads(data)["data"]["list"]#str转json数据，获取键值
    for i in result:#循环打印
        print(i["QY_ORG_CODE"]+'\t'+
              i['QY_NAME']+'\t'+
              i['QY_FR_NAME']+'\t'+
              i['QY_REGION_NAME']
              )



def main(url):
    data = get_data(url)#获取加密数据
    parse_data(data)#加密数据解析


if __name__ == '__main__':
    #加密数据指向网页
    url = 'http://jzsc.mohurd.gov.cn/api/webApi/dataservice/query/comp/list?pg=29&pgsz=15&total=0'
    main(url)

