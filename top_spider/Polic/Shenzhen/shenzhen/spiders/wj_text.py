
#小行业
def index():
    cates = [
        {"cate": "tgsgg_17341/index", "pages": 1},  # 公示公告 55
        {"cate": "tzcjd_17351/index", "pages": 1},  # 政策解读 22
        {"cate": "tflfg_17253_17253/index", "pages": 1},  # 法律法规 130

        # {"cate": "tgsgg_17341/index", "pages": 55},  # 公示公告 55
        # {"cate": "tzcjd_17351/index", "pages": 22},  # 政策解读 22
        # {"cate": "tflfg_17253_17253/index", "pages": 130},  # 法律法规 130


            ]
    return cates


def type_polic(item):
    # 新闻类型
    if '解读' in item['title']:
        item['typeId'] = 3
    elif '通告' in item['title']:
        item['typeId'] = 2
    elif '公示' in item['title']:
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









