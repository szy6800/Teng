
#小行业
def index():
    cates = [
        {"cate": "11171068", "pages": 1},#公示公告 93
        {"cate": "11171072", "pages": 1},#最新文件 20
        {"cate": "11171073", "pages": 1},#解读 13
        {"cate": "11171069", "pages": 1},#计划规划 11
                # {"cate": "11171068", "pages": 93},#公示公告 93
                # {"cate": "11171072", "pages": 20},#最新文件 20
                # {"cate": "11171073", "pages": 13},#解读 13
                # {"cate": "11171069", "pages": 11},#计划规划 11
            ]
    return cates

#分类
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
    elif '规划' in item['title']:
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







