
#小行业
def index():
    cates = [

        {"cate": "zwdt/tzgg/index", "pages": 1},#通知公告
        {"cate": "zwgk/zwwgk/glgk/zbgg/index", "pages": 1},#公告
        {"cate": "zcfg/fl/index", "pages": 1},#法律
        {"cate": "zcfg/xzfg/index", "pages" : 1},#法规
        {"cate": "zcfg/bmgz/index", "pages": 1},#部门规章
        {"cate": "zcfg/dfxfg/index", "pages": 1},#地方性法规
        {"cate": "zcfg/zcjd/index", "pages": 1},#解读

        # {"cate": "zwdt/tzgg/index", "pages": 18},#通知公告
                # {"cate": "zwgk/zwwgk/glgk/zbgg/index", "pages": 21},#公告
                # {"cate": "zcfg/fl/index", "pages": 5},#法律
                # {"cate": "zcfg/xzfg/index", "pages": 5},#法规
                # {"cate": "zcfg/bmgz/index", "pages": 4},#部门规章
                # {"cate": "zcfg/dfxfg/index", "pages": 3},#地方性法规
                # {"cate": "zcfg/zcjd/index", "pages": 7},#解读
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








