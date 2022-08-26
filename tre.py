# encoding=utf-8
import argparse
import base64
import json
import re
import ddddocr
from flask import Flask, request

parser = argparse.ArgumentParser(description="使用ddddocr搭建的最简api服务")
parser.add_argument("-p", "--port", type=int, default=9898)
parser.add_argument("--ocr", action="store_true", help="开启ocr识别")
parser.add_argument("--old", action="store_true", help="OCR是否启动旧模型")
parser.add_argument("--det", action="store_true", help="开启目标检测")

args = parser.parse_args()

app = Flask(__name__)


class Server(object):
    def __init__(self, ocr=True, det=False, old=False):
        self.ocr_option = ocr
        self.det_option = det
        self.old_option = old
        self.ocr = None
        self.det = None
        if self.ocr_option:
            print("ocr模块开启")
            if self.old_option:
                print("使用OCR旧模型启动")
                self.ocr = ddddocr.DdddOcr(old=True)
            else:
                print("使用OCR新模型启动，如需要使用旧模型，请额外添加参数  --old开启")
                self.ocr = ddddocr.DdddOcr()
        else:
            print("ocr模块未开启，如需要使用，请使用参数  --ocr开启")
        if self.det_option:
            print("目标检测模块开启")
            self.det = ddddocr.DdddOcr(det=True)
        else:
            print("目标检测模块未开启，如需要使用，请使用参数  --det开启")

    def division(self, value):
        """计算除法"""
        exp = value.split('/')
        vul1 = int(re.findall("\d+", exp[0])[0])  # 提取数字
        vul2 = int(re.findall("\d+", exp[1])[0])
        # print(vul1)
        # print(vul2)        
        return str(vul1 / vul2)

    def multiplication(self, value):
        """计算乘法"""
        exp = value.split(r'*')
        vul1 = int(re.findall("\d+", exp[0])[0])  # 提取数字
        vul2 = int(re.findall("\d+", exp[1])[0])
        # print(vul1)
        # print(vul2)        
        return str(vul1 * vul2)

    def addition(self, value):
        """计算加法"""
        exp = value.split('+')
        vul1 = int(re.findall("\d+", exp[0])[0])  # 提取数字
        vul2 = int(re.findall("\d+", exp[1])[0])
        # print(vul1)
        # print(vul2)
        return str(vul1 + vul2)

    def subtraction(self, value):
        """计算减法"""
        exp = value.split('-')
        vul1 = int(re.findall("\d+", exp[0])[0])  # 提取数字
        vul2 = int(re.findall("\d+", exp[1])[0])
        # print(vul1)
        # print(vul2)
        return str(vul1 - vul2)

    def caculation(self, img: bytes):
        if self.ocr_option:
            res = self.ocr.classification(img)
            # print(res)
            if '+' in res:
                res = self.addition(res)
            if '-' in res:
                res = self.subtraction(res)
            if 'x' in res or 'X' in res:
                res = self.multiplication(res.replace('x', '*').replace('X', '*'))
            if ' /' in res:
                res = self.division(res)
            return res
        else:
            raise Exception("ocr模块未开启")

    def classification(self, img: bytes):
        if self.ocr_option:
            return self.ocr.classification(img)
        else:
            raise Exception("ocr模块未开启")

    def detection(self, img: bytes):
        if self.det_option:
            return self.det.detection(img)
        else:
            raise Exception("目标检测模块模块未开启")

    def slide(self, target_img: bytes, bg_img: bytes, algo_type: str):
        dddd = self.ocr or self.det or ddddocr.DdddOcr(ocr=False)
        if algo_type == 'match':
            return dddd.slide_match(target_img, bg_img)
        elif algo_type == 'compare':
            return dddd.slide_comparison(target_img, bg_img)
        else:
            raise Exception(f"不支持的滑块算法类型: {algo_type}")


server = Server(ocr=args.ocr, det=args.det, old=args.old)


def get_img(request, img_type='file', img_name='image'):
    if img_type == 'b64':
        try:  # json str of multiple images
            dic = json.loads(request.get_data())
            img = base64.b64decode(dic.get(img_name).encode())
            typeid = dic.get("typeid")

        except Exception as e:  # just base64 of single image
            pass
    else:
        try:  # json str of multiple images
            dic = json.loads(request.get_data())
            img = dic.get(img_name).encode()
            typeid = dic.get("typeid")
        except Exception as e:  # just base64 of single image
            pass

    return typeid, img


def set_ret(result, ret_type='text'):
    if ret_type == 'json':
        if isinstance(result, Exception):
            return json.dumps({"status": 200, "result": "", "msg": str(result)})
        else:
            return json.dumps({"status": 200, "result": result, "msg": ""})
        # return json.dumps({"succ": isinstance(result, str), "result": str(result)})
    else:
        if isinstance(result, Exception):
            return ''
        else:
            return str(result).strip()


@app.route('/<opt>/<img_type>', methods=['POST'])
@app.route('/<opt>/<img_type>/<ret_type>', methods=['POST'])
def ocr(opt, img_type='file', ret_type='text'):
    try:
        res = get_img(request, img_type)
        typeid = res[0]
        img = res[1]
        result = ''
        if opt == 'ocr':
            if typeid == '1':  # 普通验证码
                result = server.classification(img)
            if typeid == "2":  # 计算型验证码
                result = server.caculation(img)
        elif opt == 'det':
            result = server.detection(img)
        else:
            raise f"<opt={opt}> is invalid"
        return set_ret(result, ret_type)
    except Exception as e:
        return set_ret(e, ret_type)


@app.route('/slide/<algo_type>/<img_type>', methods=['POST'])
@app.route('/slide/<algo_type>/<img_type>/<ret_type>', methods=['POST'])
def slide(algo_type='compare', img_type='file', ret_type='text'):
    try:
        target_img = get_img(request, img_type, 'target_img')
        bg_img = get_img(request, img_type, 'bg_img')
        result = server.slide(target_img, bg_img, algo_type)
        return set_ret(result, ret_type)
    except Exception as e:
        return set_ret(e, ret_type)


@app.route('/ping', methods=['GET'])
def ping():
    return "pong"



if __name__ == '__main__':
    app.run(host="127.0.0.1", port=args.port)