
#小行业
def index():
    cates = [
                {"cate": "sztax/zcwj/zxwj/common_list", "pages": 1},#最新文件
                {"cate": "sztax/zcwj/zcjd/common_list", "pages": 1},#政策解读
                {"cate": "sztax/xxgk/tzgg/common_list", "pages": 1},#通知公告
                {"cate": "sztax/zcwj/tjss/common_list", "pages": 1},#图说税收
                {"cate": "sztax/zcwj/rdwd/common_list", "pages": 1},#热点问答

                # {"cate": "sztax/zcwj/zxwj/common_list", "pages": 27},#最新文件
                # {"cate": "sztax/zcwj/zcjd/common_list", "pages": 11},#政策解读
                # {"cate": "sztax/xxgk/tzgg/common_list", "pages": 25},#通知公告
                # {"cate": "sztax/zcwj/tjss/common_list", "pages": 8},#图说税收
                # {"cate": "sztax/zcwj/rdwd/common_list", "pages": 78},#热点问答

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








