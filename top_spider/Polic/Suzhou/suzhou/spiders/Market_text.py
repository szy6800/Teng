
#小行业
def index():
    cates = [
        {"cate": "szqts/flfg/nav_list", "pages": 1},# 政策法规30
        {"cate": "szqts/fzzfjszcjd/nav_list", "pages": 1},# 政策解读4
        {"cate": "szqts/zfcgxxgs/nav_list", "pages": 1},# 政府采购信息公示4
        {"cate": "szqts/tzgg/nav_xwtz", "pages": 1},# 通知公告135
        {"cate": "szqts/scjgzt/nav_list", "pages": 1},# 市场监管专题 81



        # {"cate": "szqts/flfg/nav_list", "pages": 30},# 政策法规30
        # {"cate": "szqts/fzzfjszcjd/nav_list", "pages": 4},# 政策解读4
        # {"cate": "szqts/zfcgxxgs/nav_list", "pages": 4},# 政府采购信息公示4
        # {"cate": "szqts/tzgg/nav_xwtz", "pages": 135},# 通知公告135
        # {"cate": "szqts/scjgzt/nav_list", "pages": 81},# 市场监管专题 81

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









