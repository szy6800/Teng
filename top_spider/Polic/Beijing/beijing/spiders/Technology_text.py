
#小行业
def index():
    cates = [
        {"cate": "col1132", "pages": 1},  # 央地协同
        {"cate": "col1134", "pages": 1},  # 三城一区
        {"cate": "col1136", "pages": 1},  # 高精尖产业
        {"cate": "col1138", "pages": 1},  # 开放创新
        {"cate": "col1140", "pages": 1},    # 深化改革
        {"cate": "col736", "pages": 1},  # 通知公告
        {"cate": "col2380", "pages": 1},  # 最新政策
        {"cate": "col2962", "pages": 1},  # 北京市科技政策
        {"cate": "col2964", "pages": 1},  # 国家科技政策
        {"cate": "col2396", "pages": 1},  # 政策解读
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









