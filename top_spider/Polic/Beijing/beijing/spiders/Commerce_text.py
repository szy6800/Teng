
#小行业
def index():
    cates = [
        {"cate": "zwxx/tzgg/index", "pages": 1},  # 通知公告 37
        {"cate": "zwxx/zcfg/index", "pages": 1},  # 政策法规 29
        {"cate": "zwxx/zcfg/gfxwj/index", "pages": 1},  # 规范性文件 9
        {"cate": "zwxx/zcfg/zcwj/index", "pages": 1},  # 政策文件 9

        # {"cate": "zwxx/tzgg/index", "pages": 37},#  通知公告 37
        # {"cate": "zwxx/zcfg/index", "pages": 29},# 政策法规 29
        # {"cate": "zwxx/zcfg/gfxwj/index", "pages": 9},# 规范性文件 9
        # {"cate": "zwxx/zcfg/zcwj/index", "pages": 9},# 政策文件 9

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









