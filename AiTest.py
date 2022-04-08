# -*- coding: utf-8 -*-

# @Time : 2022/4/7 21:17
# @Author : 石张毅
# @Site : 
# @File : AiTest.py
# @Software: PyCharm 


import json
import base64
import requests

# 算法
# 构建模型
# 训练模型  ---> 需要数据集

# 找到人脸数据
def find_face(imgpath):
    http_url = 'https://api-cn.faceplusplus.com/facepp/v3/detect'
    #参数
    data = {
        'api_key': 't-SfHRRkQ_5wL0zTsMM0Joc6PlwXcHPB',
        'api_secret': 'eMRK2_lB3BZY7FUSTas3l0iGxRtd_-EM',
        'img_url':imgpath,
        'return_landmark':1
    }
    #文件
    files = {'image_file':open(imgpath,'rb')}#rb表示二进制的读取
    # 携带数据的请求我们通常使用post请求
    resp = requests.post(http_url,data=data,files=files)
    #req_con是个json格式的数据
    req_con = resp.text
    #类型转换
    this_dict = json.loads(req_con)
    faces = this_dict['faces']
    list0 = faces[0]
    #得到人脸框的数据
    rectangle = list0['face_rectangle']
    print(rectangle)
    return rectangle
# 拟合，拼接人脸
def merge_face(img_url1,img_url2,img_url3,number):
    """
    :param img_url1: 第一张图像
    :param img_url2: 第二张图像
    :param img_url3: 合并后的效果图
    :param number:相似度
    :return:
    """
    #分别获取第一张图片和第二张图片的人脸数据
    ff1 = find_face(img_url1)
    ff2 = find_face(img_url2)
    #因为参数需要是字符串类型，而ff1和ff2都是字典，我们需要格式转换
    rectangle1 = str( str(ff1['top'])+","+str(ff1['left'])+","+str(ff1['width'])+","+str(ff1['height']) )
    rectangle2 = str( str(ff2['top'])+","+str(ff2['left'])+","+str(ff2['width'])+","+str(ff2['height']) )
    print(rectangle1)
    print(rectangle2)
    f1 = open(img_url1,'rb')
    f1_64 = base64.b64encode(f1.read()) #编码
    f1.close()
    f2 = open(img_url2, 'rb')
    f2_64 = base64.b64encode(f2.read())  # 编码
    f2.close()
    #合并，我们需要使用另一个接口
    url_add = 'https://api-cn.faceplusplus.com/imagepp/v1/mergeface'

    data = {
        'api_key': 't-SfHRRkQ_5wL0zTsMM0Joc6PlwXcHPB',
        'api_secret': 'eMRK2_lB3BZY7FUSTas3l0iGxRtd_-EM',
        'template_base64':f1_64,'template_rectangle':rectangle1,
        'merge_base64':f2_64,'merge_rectangle':rectangle2,
        'merge_rate':number
    }
    resp = requests.post(url_add,data=data)
    req_con = resp.text
    # req_dict = json.loads(req_con)
    # 把json转化为字典，作用和上面那个一样，殊途同归
    req_dict = json.JSONDecoder().decode(req_con)

    result = req_dict['result']
    imgdata = base64.b64decode(result)
    file = open(img_url3,'wb')#用wb写入这张图像
    file.write(imgdata)
    file.close()


if __name__ == "__main__":

    img1 = r"D:\test\2.jpg"
    img2 = r"D:\test\1.jpg"
    img3 = r"D:\test\result3.jpg"
    merge_face(img1,img2,img3,10)
