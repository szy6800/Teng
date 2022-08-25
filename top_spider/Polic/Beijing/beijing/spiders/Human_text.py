
#小行业
def index():
    cates = [
        {"cate": "xxgk/zcwj/index", "pages": 1},  # 政策文件 24
        {"cate": "xxgk/zcjd/index", "pages": 1},  # 政策解读 18
        {"cate": "xxgk/tzgg/index", "pages": 1},  # 通知公告 50

        # {"cate": "xxgk/zcwj/index", "pages": 24},#  政策文件 24
        # {"cate": "xxgk/zcjd/index", "pages": 18},# 政策解读 18
        # {"cate": "xxgk/tzgg/index", "pages": 50},# 通知公告 5
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









