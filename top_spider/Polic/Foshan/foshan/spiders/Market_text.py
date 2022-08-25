
#小行业
def index():
    cates = [

        {"cate": "zwgk/zcfg/zcwj/index", "pages": 1},# 政策文件 3
        {"cate": "zwgk/zcfg/flfg/index", "pages": 1},# 法律法规 5
        {"cate": "zwgk/zcfg/zcjd/index", "pages": 1},# 政策解读 1
        {"cate": "zwdt/tzgg/index", "pages": 1},#  通知公告 21
        {"cate": "zmhd/yjzjjfk/index", "pages": 1},  # 通知公告 21

        # {"cate": "zwgk/zcfg/zcwj/index", "pages": 3},# 政策文件 3
        # {"cate": "zwgk/zcfg/flfg/index", "pages": 5},# 法律法规 5
        # {"cate": "zwgk/zcfg/zcjd/index", "pages": 1},# 政策解读 1
        # {"cate": "zwdt/tzgg/index", "pages": 21},#  通知公告 21
        # {"cate": "zmhd/yjzjjfk/index", "pages": 10},#  通知公告 21

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









