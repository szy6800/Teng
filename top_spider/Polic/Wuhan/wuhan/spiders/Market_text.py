
#小行业
def index():
    cates = [
        {"cate": "ztzl/bhfw/zlzcfg/index", "pages": 1},# 政策法规3
        {"cate": "ztzl/bhfw/zscqjs/zscq2020/index", "pages": 1},# 政策解读3
        {"cate": "zwgk_65/jggg/tzgg/index", "pages": 1},# 通知公告188
        {"cate": "zwgk_65/jggg/fwml/index", "pages": 1},# 电动车3
        {"cate": "zwgk_65/zcfgyjd/gfxwjsjk/index", "pages": 1},# 规范性文件3
        {"cate": "zwgk_65/zcfgyjd/zcfg_6163/index", "pages": 1},# 其他主动公开文件6
        {"cate": "zwgk_65/zcfgyjd/zcjd/index", "pages": 1},# 政策解读3

        # {"cate": "ztzl/bhfw/zlzcfg/index", "pages": 3},# 政策法规3
        # {"cate": "ztzl/bhfw/zscqjs/zscq2020/index", "pages": 3},# 政策解读3
        # {"cate": "zwgk_65/jggg/tzgg/index", "pages": 1},# 通知公告188
        # {"cate": "zwgk_65/jggg/fwml/index", "pages": 3},# 电动车3
        # {"cate": "zwgk_65/zcfgyjd/gfxwjsjk/index", "pages": 3},# 规范性文件3
        # {"cate": "zwgk_65/zcfgyjd/zcfg_6163/index", "pages": 6},# 其他主动公开文件6
        # {"cate": "zwgk_65/zcfgyjd/zcjd/index", "pages": 3},# 政策解读3

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









