
#小行业
def index():
    cates = [
        {"cate": "scjdglj/zwgkzdgz/zcyjd/tzgg/glist", "pages": 1},# 公示公告 199
        {"cate": "scjdglj/zwgkzdgz/bzhgz/glist", "pages": 1},# 标准化工作 2
        {"cate": "scjdglj/zwgkzdgz/zscqggfwpt/glist", "pages": 1},# 知识产权工作 2
        {"cate": "scjdglj/zwgkzdgz/zcyjd/zcjd/glist", "pages": 1},# 政策解读 4
        {"cate": "scjdglj/zwgkzdgz/fdzdgknr/flfggz/glist", "pages": 1},# 法律法规规章 7
        {"cate": "scjdglj/bmfw/xzsp/spxxgs/glist", "pages": 1},# 审批公示 153






        # {"cate": "scjdglj/zwgkzdgz/zcyjd/tzgg/glist", "pages": 199},# 公示公告 199
        # {"cate": "scjdglj/zwgkzdgz/bzhgz/glist", "pages": 2},# 标准化工作 2
        # {"cate": "scjdglj/zwgkzdgz/zscqggfwpt/glist", "pages": 2},# 知识产权工作 2
        # {"cate": "scjdglj/zwgkzdgz/zcyjd/zcjd/glist", "pages": 4},# 政策解读 4
        # {"cate": "scjdglj/zwgkzdgz/fdzdgknr/flfggz/glist", "pages": 7},# 法律法规规章 7
        # {"cate": "scjdglj/bmfw/xzsp/spxxgs/glist", "pages": 153},# 审批公示 153

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









