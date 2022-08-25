
#小行业
def index():
    cates = [

        {"cate": "jinrongban/c139004/zcfg1", "pages": 1},  # 政策法规21
        {"cate": "jinrongban/c139005/zcfg_list", "pages": 1},  # 政策解读8
        {"cate": "jinrongban/c139009/zcfg", "pages": 1},  # 政务公开 21
        {"cate": "jinrongban/c139013/list", "pages": 1},  # 通知公告 12

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









