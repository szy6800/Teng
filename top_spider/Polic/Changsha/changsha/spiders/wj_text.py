
#小行业
def index():
    cates = [
        {"cate": "zxzx_0/tzgg_131288/rsrc_131289/index", "pages": 1},  # 人事人才 30
        {"cate": "zxzx_0/tzgg_131288/shbx_131290/index", "pages": 1},  # 社会保险 29
        {"cate": "zxzx_0/tzgg_131288/ldjy_131291/index", "pages": 1},  # 劳动就业 29
        {"cate": "zxzx_0/tzgg_131288/ldgx_131292/index", "pages": 1 },  # 劳动关系 29
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









