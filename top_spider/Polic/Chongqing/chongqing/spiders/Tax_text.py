
#小行业
def index():
    cates = [

        {"cate": "cqtax/zcwj/zxwj/index", "pages": 1},# 最新文件27
        {"cate": "cqtax/zcwj/zcjd/index", "pages": 1},# 政策解读
        {"cate": "cqtax/zcwj/tjss/index", "pages": 1},# 图解税收
        # {"cate": "cqtax/zcwj/rdwd/zzs/index", "pages": 1},# 热点问答 增值税
        # {"cate": "cqtax/zcwj/rdwd/qysds/index", "pages": 1},# 热点问答 企业所得税
        # {"cate": "cqtax/zcwj/rdwd/xfs/index", "pages": 1},# 热点问答 消费税
        # {"cate": "cqtax/zcwj/rdwd/clgzs/index", "pages": 1},# 热点问答 车辆购置税
        # {"cate": "cqtax/zcwj/rdwd/hbs/index", "pages": 1},# 热点问答 环保税
        # {"cate": "cqtax/zcwj/rdwd/qt/index", "pages": 1},# 热点问答 其他
        # {"cate": "cqtax/zcwj/zczy/index", "pages": 1},# 热点问答 政策指引
        # {"cate": "cqtax/zcwj/zczc/", "pages": 1},# 热点问答 支持疫情防控政策文件
        # {"cate": "cqtax/zcwj/zcwd/", "pages": 1},# 热点问答 支持疫情防控热点问答
        # {"cate": "cqtax/xxgk/tzgg/index", "pages": 1},# 通知公告


                # {"cate": "cqtax/zcwj/zxwj/index", "pages": 27},# 最新文件27
                # {"cate": "cqtax/zcwj/zcjd/index", "pages": 13},# 政策解读
                # {"cate": "cqtax/zcwj/tjss/index", "pages": 37},# 图解税收
                # {"cate": "cqtax/zcwj/rdwd/zzs/index", "pages": 18},# 热点问答 增值税
                # {"cate": "cqtax/zcwj/rdwd/qysds/index", "pages": 7},# 热点问答 企业所得税
                # {"cate": "cqtax/zcwj/rdwd/xfs/index", "pages": 6},# 热点问答 消费税
                # {"cate": "cqtax/zcwj/rdwd/clgzs/index", "pages": 6},# 热点问答 车辆购置税
                # {"cate": "cqtax/zcwj/rdwd/hbs/index", "pages": 5},# 热点问答 环保税
                # {"cate": "cqtax/zcwj/rdwd/qt/index", "pages": 10},# 热点问答 其他
                # {"cate": "cqtax/zcwj/zczy/index", "pages": 3},# 热点问答 政策指引
                # {"cate": "cqtax/zcwj/zczc/", "pages": 1},# 热点问答 支持疫情防控政策文件
                # {"cate": "cqtax/zcwj/zcwd/", "pages": 1},# 热点问答 支持疫情防控热点问答
                # {"cate": "cqtax/xxgk/tzgg/index", "pages": 18},# 通知公告

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









