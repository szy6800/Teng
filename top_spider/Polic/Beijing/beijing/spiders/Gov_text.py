
#小行业
def index():
    cates = [
        {"cate": "zhengce/zhengcefagui/", "pages": 1},  # 政策文件（最新政策）
        {"cate": "zhengce/zfwj/", "pages": 1},  # 市政府文件
        {"cate": "zhengce/zfwj/zfwj2016/bgtwj/", "pages": 1},  # 市办公厅文件 10
        {"cate": "zhengce/zfwj/zfwj2016/szfl/", "pages": 1},  # 财政预决算 10
        {"cate": "so/zcdh/zcjd/", "pages": 1},  # 政策解读 10
        {"cate": "zhengce/dfxfg/", "pages": 1},  # 财政预决算 10
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









