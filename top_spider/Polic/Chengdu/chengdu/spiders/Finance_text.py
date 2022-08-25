
#小行业
def index():
    cates = [
        {"cate": "cdsczj/zjwj/jgsz_list", "pages": 1},  # 资金文件 10
        {"cate": "cdsczj/c116712/jgsz_list", "pages": 1},  # 公告公示 15
        {"cate": "cdsczj/c116727/list1", "pages": 1},  # 政策文件最新信息公开 9
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









