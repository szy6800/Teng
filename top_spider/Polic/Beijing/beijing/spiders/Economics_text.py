
#小行业
def index():
    cates = [
        {"cate": "zwgk/zcwj/gjzc/index", "pages": 1},  # 国家政策 9
        {"cate": "zwgk/zcwj/bjszc/index", "pages": 1},  # 北京市政策 8
        {"cate": "zwgk/flfg/gjflfggz/fl/index", "pages": 1},  # 法律 2
        {"cate": "zwgk/flfg/gjflfggz/xzfg/index", "pages": 1},  # 行政法规 3
        {"cate": "zwgk/flfg/gjflfggz/bmgz/index", "pages": 1},  # 部门规章 4
        {"cate": "zwgk/zcjd/index", "pages": 1},  # 政策解读 6

        # {"cate": "zwgk/zcwj/gjzc/index", "pages": 9},#  国家政策 9
        # {"cate": "zwgk/zcwj/bjszc/index", "pages": 8},# 北京市政策 8
        # {"cate": "zwgk/flfg/gjflfggz/fl/index", "pages": 2},# 法律 2
        # {"cate": "zwgk/flfg/gjflfggz/xzfg/index", "pages": 3},# 行政法规 3
        # {"cate": "zwgk/flfg/gjflfggz/bmgz/index", "pages": 4},# 部门规章 4
        # {"cate": "zwgk/zcjd/index", "pages": 6},# 政策解读 6
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









