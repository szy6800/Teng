
#小行业
def index():
    cates = [

        {"cate": "zfxxgk_225/fdzdgknr/lzyj/list", "pages": 1},  # 履职依据q19/
        {"cate": "zfxxgk_225/fdzdgknr/gsgg/xzxk/list", "pages": 1},  # 公示公告 行政许可32
        {"cate": "zfxxgk_225/fdzdgknr/gsgg/jdcj/list", "pages": 1},  # 公示公告 监督检查
        {"cate": "zfxxgk_225/fdzdgknr/gsgg/xzcf/list", "pages": 1},  # 公示公告 行政处罚

        {"cate": "zfxxgk_225/fdzdgknr/gsgg/qtgg/list", "pages": 1},  # 公示公告 其他公示公告
        {"cate": "zfxxgk_225/fdzdgknr/gsgg/xzfyjds/list", "pages": 1},  # 公示公告 行政复议决定书
        {"cate": "zfxxgk_225/fdzdgknr/gsgg/qxcpzh/list", "pages": 1},  # 公示公告 缺陷产品召回
        {"cate": "zfxxgk_225/fdzdgknr/gsgg/jlbznlsm/list", "pages": 1},  # 公示公告 计量保证能力声明3

        {"cate": "zfxxgk_225/zcwj/index", "pages": 1},  # 政策文件
        {"cate": "zfxxgk_225/zcjd/index", "pages": 1},  # 政策解读
        {"cate": "zfxxgk_225/zcjd/index", "pages": 1},  # 制度文件汇编







        # {"cate": "zfxxgk_225/fdzdgknr/lzyj/list", "pages": 19},  # 履职依据q19/
        # {"cate": "zfxxgk_225/fdzdgknr/gsgg/xzxk/list", "pages": 32},  # 公示公告 行政许可32
        # {"cate": "zfxxgk_225/fdzdgknr/gsgg/jdcj/list", "pages": 19},  # 公示公告 监督检查
        # {"cate": "zfxxgk_225/fdzdgknr/gsgg/xzcf/list", "pages": 19},  # 公示公告 行政处罚

        # {"cate": "zfxxgk_225/fdzdgknr/gsgg/qtgg/list", "pages": 22},  # 公示公告 其他公示公告
        # {"cate": "zfxxgk_225/fdzdgknr/gsgg/xzfyjds/list", "pages": 7},  # 公示公告 行政复议决定书
        # {"cate": "zfxxgk_225/fdzdgknr/gsgg/qxcpzh/list", "pages": 8},  # 公示公告 缺陷产品召回
        # {"cate": "zfxxgk_225/fdzdgknr/gsgg/jlbznlsm/list", "pages": 3},  # 公示公告 计量保证能力声明3
        #
        # {"cate": "zfxxgk_225/zcwj/index", "pages": 5},  # 政策文件
        # {"cate": "zfxxgk_225/zcjd/index", "pages": 3},  # 政策解读
        # {"cate": "zfxxgk_225/zcjd/index", "pages": 1},  # 制度文件汇编

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








