
#小行业
def index():
    cates = [
        {"cate": "tjsscjdglwyh_52651/xwdt/gs/index", "pages": 1},#公示 20
        {"cate": "tjsscjdglwyh_52651/xwdt/tg/index", "pages": 1},#通告
        {"cate": "tjsscjdglwyh_52651/xwdt/gztz/index", "pages": 1},#工作通知
        {"cate": "tjsscjdglwyh_52651/xwdt/zlccbg/index", "pages": 1},# 质量抽查报告
        {"cate": "tjsscjdglwyh_52651/zwgk/zfgznew/gjzc/index", "pages": 1},#  国家政策
        {"cate": "tjsscjdglwyh_52651/zwgk/zfgznew/sjzc/index", "pages": 1},#  市级政策
        {"cate": "tjsscjdglwyh_52651/zwgk/zfgznew/bdwwjnew/gzwjnew_1/index", "pages": 1},#  工作文件
        {"cate": "tjsscjdglwyh_52651/zwgk/zfgznew/bdwwjnew/gfxwjnew/index", "pages": 1},#  规范性文件
        {"cate": "tjsscjdglwyh_52651/zwgk/zfgznew/bdwwjnew/sjwwj_1/index", "pages": 1},#  政策文件
        {"cate": "tjsscjdglwyh_52651/zwgk/zfgznew/bdwwjnew/jdhynew/index", "pages": 1},#  政策解读
        # 天津市
        # {"cate": "tjsscjdglwyh_52651/xwdt/gs/index", "pages": 20},#公示 20
        # {"cate": "tjsscjdglwyh_52651/xwdt/tg/index", "pages": 20},#通告
        # {"cate": "tjsscjdglwyh_52651/xwdt/gztz/index", "pages": 11},#工作通知
        # {"cate": "tjsscjdglwyh_52651/xwdt/zlccbg/index", "pages": 8},# 质量抽查报告
        # {"cate": "tjsscjdglwyh_52651/zwgk/zfgznew/gjzc/index", "pages": 2},#  国家政策
        # {"cate": "tjsscjdglwyh_52651/zwgk/zfgznew/sjzc/index", "pages": 2},#  市级政策
        # {"cate": "tjsscjdglwyh_52651/zwgk/zfgznew/bdwwjnew/gzwjnew_1/index", "pages": 20},#  工作文件
        # {"cate": "tjsscjdglwyh_52651/zwgk/zfgznew/bdwwjnew/gfxwjnew/index", "pages": 4},#  规范性文件
        # {"cate": "tjsscjdglwyh_52651/zwgk/zfgznew/bdwwjnew/sjwwj_1/index", "pages": 20},#  政策文件
        # {"cate": "tjsscjdglwyh_52651/zwgk/zfgznew/bdwwjnew/jdhynew/index", "pages": 4},#  政策解读









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
    elif '规划1' in item['title']:
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







