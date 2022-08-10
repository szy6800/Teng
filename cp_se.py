import requests
import execjs
import json


class BaiDuTranslateWeb:
    def __init__(self):
        self.url = "https://fanyi.baidu.com/v2transapi"
        self.headers = {
            "Cookie": "",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36"
        }
        self.data = {
            "from": "zh",
            "to": "en",
            "query": None,
            "transtype": "translang",
            "simple_means_flag": 3,
            "sign": None,
            "token": "300f465c88543c5218f056447a33a348"
        }

    def get_baidu_sign(self):
        with open("baidusign.js") as f:
            jsData = f.read()
            sign = execjs.compile(jsData).call("e", self.input)
            return sign

    def run(self):
        self.input = input("请输入要翻译的内容：")
        self.get_baidu_sign()
        self.data["query"] = self.input
        self.data["sign"] = self.get_baidu_sign()
        response = requests.post(url=self.url, data=self.data, headers=self.headers)
        self.result_strs = response.content.decode()

    def get_translate_result(self):
        result_dict = json.loads(self.result_strs)
        if 'trans_result' in result_dict:
            result_dict = result_dict['trans_result']['data'][0] if len(
                result_dict['trans_result']['data']) > 0 else None
            result_dict = result_dict['result'][0] if len(result_dict['result']) > 0 else None
            result = result_dict[1] if len(result_dict) > 1 else None
            print("翻译结果为：")
            print(result)
        else:
            print("请输入内容再进行翻译")


if __name__ == '__main__':
    while True:
        baidutranlate = BaiDuTranslateWeb()
        baidutranlate.run()
        baidutranlate.get_translate_result()