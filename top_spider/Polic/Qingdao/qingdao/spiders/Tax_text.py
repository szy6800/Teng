
#小行业
def index():
    cates = [
        {"cate": "xxgk2019/tztg/index_1002", "pages": 1},# 通知公告
        {"cate": "zxfb2019/index_1002", "pages": 1},# 通知公告
        {"cate": "ssfg2019/zxwj/index", "pages": 1},# 最新文件
        {"cate": "ssfg2019/zcjd/index", "pages": 1},# 政策解读
        {"cate": "ssfg2019/yhzc/index", "pages": 1},#优惠政策
        {"cate": "ssfg2019/gfxwj/index", "pages": 1},#规范性文件

        {"cate": "bsfw2019/bszn/index", "pages": 1},#3 办税指南
        {"cate": "bsfw2019/bszn/fpbl/index", "pages": 1},#发票办理
        {"cate": "bsfw2019/bszn/xxbg/index", "pages": 1},#信息报告
        {"cate": "bsfw2019/bszn/sbns/index", "pages": 1},#申报纳税
        {"cate": "bsfw2019/bszn/yhbl/index", "pages": 1},#优惠办理
        {"cate": "bsfw2019/bszn/sszyfwgf/index", "pages": 1},#涉税专业服务
        {"cate": "bsfw2019/bszn/sszx/index", "pages": 1},#涉税（费）咨询
        {"cate": "bsfw2019/bszn/qszx/index", "pages": 1},#税务注销
        {"cate": "bsfw2019/bszn/cktms/index", "pages": 1},#出口退（免）税
        {"cate": "bsfw2019/bszn/gjss/index", "pages": 1},#国际税收
        {"cate": "ssfg2019/cjwt/index_1004", "pages": 1},#热点问答

        {"cate": "qdsw_shinan/xxgk2019/tztg/index_657", "pages": 1},#市南区
        {"cate": "qdsw_shibei/xxgk2019/tztg/index_676", "pages": 1},#市北区
         {"cate": "qdsw_licang/xxgk2019/tztg/index_698", "pages": 1},#李沧区
        {"cate": "qdsw_laoshan/xxgk2019/tztg/index_724", "pages": 1},#崂山区！！！！！！！
         {"cate": "qdsw_chengyang/xxgk2019/tztg/index_748", "pages": 1},#城阳区
         {"cate": "qdsw_kaifaqu/xxgk2019/tztg/index_817", "pages": 1},#开发区
         {"cate": "qdsw_baoshui/xxgk2019/tztg/index_855", "pages": 1},#保税区
         {"cate": "qdsw_gaoxin/xxgk2019/tztg/index_834", "pages": 1},#高新区
         {"cate": "qdsw_huangdao/xxgk2019/tztg/index_769", "pages": 1},#黄岛区
         {"cate": "qdsw_jimo/xxgk2019/tztg/index_786", "pages": 1},#即墨区
         {"cate": "qdsw_pingdu/xxgk2019/tztg/index_906", "pages": 1},#平度
         {"cate": "qdsw_laixi/xxgk2019/tztg/index_921", "pages": 1},#莱西

                # {"cate": "xxgk2019/tztg/index_1002", "pages": 25},# 通知公告
                # {"cate": "zxfb2019/index_1002", "pages": 35},# 通知公告
                # {"cate": "ssfg2019/zxwj/index", "pages": 25},# 最新文件
                # {"cate": "ssfg2019/zcjd/index", "pages": 9},# 政策解读
                # {"cate": "ssfg2019/yhzc/index", "pages": 1},#优惠政策
                # {"cate": "ssfg2019/gfxwj/index", "pages": 3},#规范性文件
                #
                # {"cate": "bsfw2019/bszn/index", "pages": 13},#3 办税指南
                # {"cate": "bsfw2019/bszn/fpbl/index", "pages": 2},#发票办理
                # {"cate": "bsfw2019/bszn/xxbg/index", "pages": 3},#信息报告
                # {"cate": "bsfw2019/bszn/sbns/index", "pages": 4},#申报纳税
                # {"cate": "bsfw2019/bszn/yhbl/index", "pages": 1},#优惠办理
                # {"cate": "bsfw2019/bszn/sszyfwgf/index", "pages": 1},#涉税专业服务
                # {"cate": "bsfw2019/bszn/sszx/index", "pages": 1},#涉税（费）咨询
                # {"cate": "bsfw2019/bszn/qszx/index", "pages": 1},#税务注销
                # {"cate": "bsfw2019/bszn/cktms/index", "pages": 2},#出口退（免）税
                # {"cate": "bsfw2019/bszn/gjss/index", "pages": 2},#国际税收
                # {"cate": "ssfg2019/cjwt/index_1004", "pages": 13},#热点问答

                # {"cate": "qdsw_shinan/xxgk2019/tztg/index_657", "pages": 14},#市南区
                # {"cate": "qdsw_shibei/xxgk2019/tztg/index_676", "pages": 13},#市北区
               #  {"cate": "qdsw_licang/xxgk2019/tztg/index_698", "pages": 16},#李沧区
               # {"cate": "qdsw_laoshan/xxgk2019/tztg/index_724", "pages": 10},#崂山区！！！！！！！
               #  {"cate": "qdsw_chengyang/xxgk2019/tztg/index_748", "pages": 10},#城阳区
               #  {"cate": "qdsw_kaifaqu/xxgk2019/tztg/index_817", "pages": 6},#开发区
               #  {"cate": "qdsw_baoshui/xxgk2019/tztg/index_855", "pages": 7},#保税区
               #  {"cate": "qdsw_gaoxin/xxgk2019/tztg/index_834", "pages": 8},#高新区
               #  {"cate": "qdsw_huangdao/xxgk2019/tztg/index_769", "pages": 12},#黄岛区
               #  {"cate": "qdsw_jimo/xxgk2019/tztg/index_786", "pages": 16},#即墨区
               #  {"cate": "qdsw_pingdu/xxgk2019/tztg/index_906", "pages": 7},#平度
               #  {"cate": "qdsw_laixi/xxgk2019/tztg/index_921", "pages": 8},#莱西

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









