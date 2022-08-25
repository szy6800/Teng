
#小行业
def index():
    cates = [

        {"cate": "xxgk/qt/tzgg/", "pages": 1},  # 通知
        {"cate": "xxgk/zcwj/scjgfg/", "pages": 1},  # 法规
        {"cate": "xxgk/zcwj/zcjd/", "pages": 1},  # 解读
        {"cate": "xxgk/ghjh/zxgh_1/", "pages": 1},  # 计划

               #  {"cate": "xxgk/qt/tzgg/", "pages": 21},#通知
               # {"cate": "xxgk/zcwj/scjgfg/", "pages": 20},#法规
               #  {"cate": "xxgk/zcwj/zcjd/", "pages": 5},#解读
               #  {"cate": "xxgk/ghjh/zxgh_1/", "pages": 2},#计划
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
    elif '？' in item['title']:
        item['typeId'] = 4
    elif '法' in item['title']:
        item['typeId'] = 5
    elif '条例' in item['title']:
        item['typeId'] = 5
    else:
        item['typeId'] = 1

    return item['typeId']








