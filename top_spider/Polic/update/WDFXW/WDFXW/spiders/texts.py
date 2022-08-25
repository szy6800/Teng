import re
import requests
# sss = '''
#    fileCategoryName: '劳动劳务||||', //资料分类名称
#         },
#         page: {
#             status: '0',
#             state: '4',
#             vipDiscountFlag: '1',
#             preRead: '3',
#             isConvert: '1',
#             moneyPrice: '1',
#             isDownload: '',
#             cmsOnOff: '',
#             isHasCollect: '',
#             collectNum: '9090',
#         },
#         // 背景图
#         decorateBgUrl: 'https://ishare-cms-file.oss-cn-beijing.aliyuncs.com/market/190E7cnpyV.png',
#         // 是否svg
#         isSvgContent: true,
#         // 背景图间距
#         transcodePosition: {"top":121,"left":118,"right":118,"bottom":124,"width":830},
#         // 内容数据总数
#         transcodeContentTotal: 3,
#         // 内容数据列表
#         transcodeContentList: ["https://swf.ishare.down.sina.com.cn/ZQ4ESoDiT6m.svg?ssig=QFB4Qxff5U&Expires=1628854980&KID=sina,ishare&range=0-10803","https://swf.ishare.down.sina.com.cn/ZQ4ESoDiT6m.svg?ssig=QFB4Qxff5U&Expires=1628854980&KID=sina,ishare&range=10805-22060","https://swf.ishare.down.sina.com.cn/ZQ4ESoDiT6m.svg?ssig=QFB4Qxff5U&Expires=1628854980&KID=sina,ishare&range=22062-31712"],
#         origin: {}
# '''

# result = re.findall('https:\/\/swf.ishare.down.sina.com.cn\/.*?\?ssig=.*?&Expires=\d+&KID=.*?,ishare&range=[0-9-]+',sss)
# # print(result)
# for i in result:
#     res = requests.get(i)
#     print(res.text)

# for i in a:
#     print(i)


