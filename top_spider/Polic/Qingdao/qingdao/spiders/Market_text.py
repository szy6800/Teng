
#小行业
def index():
    cates = [

        {"cate": "n28356084/n32567971/n32567978/index", "pages": 1},#23 通知
        {"cate": "n28356084/n32567971/n32567979/n32568015/index", "pages": 1},#10 公告1
        {"cate": "n28356084/n32567971/n32567979/n32568453/index", "pages": 1},#3 公告2
        {"cate": "n28356084/n32567971/n32567979/n32568016/index", "pages": 1},#16 公告3
        {"cate": "n28356084/n32567971/n32567979/n32568017/index", "pages": 1},#4 公告4
        {"cate": "n28356084/n32567971/n32567979/n32568019/index", "pages": 1},#3 公告5
        #
        {"cate": "n28356084/n32567971/n32567980/index", "pages": 1},#2 行政文件
        {"cate": "n28356084/n32567971/n32568020/index", "pages": 1},#5 法律法规
        {"cate": "n28356084/n32567971/n32567982/index", "pages": 1},#3 解读




                # {"cate": "n28356084/n32567971/n32567978/index", "pages": 25},#23 通知
                # {"cate": "n28356084/n32567971/n32567979/n32568015/index", "pages": 11},#10 公告1
                # {"cate": "n28356084/n32567971/n32567979/n32568453/index", "pages": 4},#3 公告2
                # {"cate": "n28356084/n32567971/n32567979/n32568016/index", "pages": 20},#16 公告3
                # {"cate": "n28356084/n32567971/n32567979/n32568017/index", "pages": 5},#4 公告4
                # {"cate": "n28356084/n32567971/n32567979/n32568019/index", "pages": 4},#3 公告5
                # #
                # {"cate": "n28356084/n32567971/n32567980/index", "pages": 3},#2 行政文件
                # {"cate": "n28356084/n32567971/n32568020/index", "pages": 6},#5 法律法规
                # {"cate": "n28356084/n32567971/n32567982/index", "pages": 4},#3 解读
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









