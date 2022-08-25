
#小行业
def index():
    cates = [
        {"cate": "tzgg/", "pages": 1}, #通知公告
        {"cate": "xxgk/zxxxgk/", "pages": 1},#最新信息公开
        {"cate": "xxgk/zfxxgkml/zfgkzcwj/zwgkxzgfxwj/", "pages": 1},#行政规范性文件
        {"cate": "xxgk/zfxxgkml/zfgkzcwj/zwgzdt/", "pages": 1},#其他文件
        {"cate": "xxgk/zfxxgkml/zfgkzcwj/zcjd/", "pages": 1},#政策解读
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









