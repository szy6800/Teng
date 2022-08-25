
#小行业
def index():
    cates = [
        {"cate": "hbsw/wuhan/tzgg/sjtzgg/index", "pages": 1},# 通知公告 10
        {"cate": "hbsw/wuhan/tzgg/qjtzgg/index", "pages": 1},# 区局通知公告1
        {"cate": "hbsw/zcwj/zxwj/index", "pages": 1},# 最新文件25
        {"cate": "hbsw/zcwj/zcjd/index", "pages": 1},# 政策解读10
        {"cate": "hbsw/zcwj/tjss/index", "pages": 1},# 图解税收11
        {"cate": "hbsw/zcwj/rdwd/index", "pages": 1},# 热点问答18
        {"cate": "hbsw/xxgk/tzgg/index", "pages": 1},# 通知公告13
        {"cate": "hbsw/xxgk/zfcg/index", "pages": 1},  # 政府采购14


        # {"cate": "hbsw/wuhan/tzgg/sjtzgg/index", "pages": 10},# 通知公告 10
        # {"cate": "hbsw/wuhan/tzgg/qjtzgg/index", "pages": 1},# 区局通知公告1
        # {"cate": "hbsw/zcwj/zxwj/index", "pages": 25},# 最新文件25
        # {"cate": "hbsw/zcwj/zcjd/index", "pages": 10},# 政策解读10
        # {"cate": "hbsw/zcwj/tjss/index", "pages": 11},# 图解税收11
        # {"cate": "hbsw/zcwj/rdwd/index", "pages": 18},# 热点问答18
        # {"cate": "hbsw/xxgk/tzgg/index", "pages": 13},# 通知公告13
        # {"cate": "hbsw/xxgk/zfcg/index", "pages": 14},# 政府采购14

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









