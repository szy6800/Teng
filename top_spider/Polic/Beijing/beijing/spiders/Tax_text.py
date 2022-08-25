# -*- coding: utf-8 -*-


def file_type(item):
    if '解读' in item['title']:
        item['typeId'] = 3
    elif '通告' in item['title']:
        item['typeId'] = 2
    elif '公告' in item['title']:
        item['typeId'] = 2
    elif '通知' in item['title']:
        item['typeId'] = 1
    elif '服务' in item['title']:
        item['typeId'] = 4
    elif '指南' in item['title']:
        item['typeId'] = 4
    elif '？' in item['title']:
        item['typeId'] = 4
    elif '法' in item['title']:
        item['typeId'] = 5
    elif '条例' in item['title']:
        item['typeId'] = 5
    else:
        item['typeId'] = 1
    return item['typeId']

def index():
    cates = [
                #
                # {"cate": "增值税", "pages": 1},
                # {"cate": "消费税", "pages": 1},
                # {"cate": "企业所得税", "pages": 1},
                # {"cate": "个人所得税", "pages": 1},
                # {"cate": "资源税", "pages": 1},
                # {"cate": "城市维护建设税", "pages": 1},
                # {"cate": "房产税", "pages": 1},
                # {"cate": "印花税", "pages": 1},
                # {"cate": "城镇土地使用税", "pages": 1},
                # {"cate": "土地增值税", "pages": 1},
                # {"cate": "车船税", "pages": 1},
                # {"cate": "车辆购置税", "pages": 1},
                # {"cate": "烟叶税", "pages": 1},
                # {"cate": "耕地占用税", "pages": 1},
                # {"cate": "契税", "pages": 1},
                # {"cate": "环境保护税", "pages": 1},
                # {"cate": "进出口税收", "pages": 1},



                # {"cate": "增值税", "pages": 72},
                # {"cate": "消费税", "pages": 14},
                # {"cate": "企业所得税", "pages": 49},
                # {"cate": "个人所得税", "pages": 32},
                # {"cate": "资源税", "pages": 9},
                # {"cate": "城市维护建设税", "pages": 7},
                # {"cate": "房产税", "pages": 9},
                # {"cate": "印花税", "pages": 17},
                # {"cate": "城镇土地使用税", "pages": 13},
                # {"cate": "土地增值税", "pages": 6},
                # {"cate": "车船税", "pages": 6},
                # {"cate": "车辆购置税", "pages": 12},
                # {"cate": "烟叶税", "pages": 1},
                # {"cate": "耕地占用税", "pages": 3},
                # {"cate": "契税", "pages": 13},
                # {"cate": "环境保护税", "pages": 1},
                # {"cate": "进出口税收", "pages": 31},

            ]
    return cates

def type_polic(item,news_type):
    if '增值税' == news_type:
        item['typeId'] = 1
    elif '消费税' in news_type:
        item['typeId'] = 2
    elif '企业所得税' in news_type:
        item['typeId'] = 3
    elif '个人所得税' in news_type:
        item['typeId'] = 4
    elif '资源税' in news_type:
        item['typeId'] = 5
    elif '城市维护建设税' in news_type:
        item['typeId'] = 6
    elif '房产税' in news_type:
        item['typeId'] = 7
    elif '印花税' in news_type:
        item['typeId'] = 8
    elif '城镇土地使用税' in news_type:
        item['typeId'] = 9
    elif '土地增值税' == news_type:
        item['typeId'] = 10
    elif '车船税' in news_type:
        item['typeId'] = 11
    elif '车辆购置税' in news_type:
        item['typeId'] = 12
    elif '烟叶税' in news_type:
        item['typeId'] = 13
    elif '耕地占用税' in news_type:
        item['typeId'] = 14
    elif '契税' in news_type:
        item['typeId'] = 15
    elif '环境保护税' in news_type:
        item['typeId'] = 16
    elif '进出口税收' in news_type:
        item['typeId'] = 17
    else:
        item['typeId'] = 0

    return item['typeId']
