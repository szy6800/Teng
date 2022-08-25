
#小行业
def index():
    cates = [
        {"cate": "cs/lists/20190719067982/", "pages": 1},# 通知公告 7
        {"cate": "cs/lists/20190719067952/", "pages": 1},# 限期改正公告 20
        {"cate": "lists/20190725027557/", "pages": 1},# 最新文件 35 省局
        {"cate": "lists/20190629092930/", "pages": 1},# 政策解读 11 省局
        {"cate": "lists/20190629092947/", "pages": 1},# 图解税收 20 省局
        {"cate": "lists/20190808056618/", "pages": 1},  # 热点问答 29 省局

        # {"cate": "cs/lists/20190719067982/", "pages": 7},# 通知公告 7
        # {"cate": "cs/lists/20190719067952/", "pages": 20},# 限期改正公告 20
        # {"cate": "lists/20190725027557/", "pages": 35},# 最新文件 35 省局
        # {"cate": "lists/20190629092930/", "pages": 11},# 政策解读 11 省局
        # {"cate": "lists/20190629092947/", "pages": 20},# 图解税收 20 省局
        # {"cate": "lists/20190808056618/", "pages": 29},# 热点问答 29 省局
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









