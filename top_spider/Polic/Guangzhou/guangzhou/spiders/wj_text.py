
#小行业
def index():
    cates = [
        # {"cate": "xxgk/tzgg/tz/index", "pages": 21},  # 通知  21
        # {"cate": "xxgk/tzgg/zwgg/index", "pages": 21},  # 政务公告  21
        # {"cate": "xxgk/tzgg/ywgs/index", "pages": 21},  # 业务公示  21

        {"cate": "xxgk/tzgg/tz/index", "pages": 1},  # 通知  21
        {"cate": "xxgk/tzgg/zwgg/index", "pages": 1},  # 政务公告  21
        {"cate": "xxgk/tzgg/ywgs/index", "pages": 1},  # 业务公示  21


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









