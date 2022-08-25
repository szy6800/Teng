
#小行业
def index():
    cates = [
        {"cate": "lmdm=030001&fjdm=11200000000&page=", "pages": 1},#公示37

        {"cate": "lmdm=030002&fjdm=11200000000&page=", "pages": 1},#政策解读

        {"cate": "lmdm=030005&fjdm=11200000000&page=", "pages": 1},# 热点问答

        {"cate": "lmdm=030006&fjdm=11200000000&page=", "pages": 1},# 税收规范性文件

        {"cate": "lmdm=010003&fjdm=11200000000&page=", "pages": 1},# 通知公告
        {"cate": "lmdm=01000501&fjdm=11200000000&page=", "pages": 1},# 采购信息公告

        #各个区
        {"cate": "lmdm=010003&fjdm=11241000000&page=", "pages": 1},# 和平区6
        {"cate": "lmdm=010003&fjdm=11242000000&page=", "pages": 1},# 河东区
        {"cate": "lmdm=010003&fjdm=11243000000&page=", "pages": 1},# 河西区/
        {"cate": "lmdm=010003&fjdm=11244000000&page=", "pages": 1},# 南开区
        {"cate": "lmdm=010003&fjdm=11245000000&page=", "pages": 1},# 河北区
        {"cate": "lmdm=010003&fjdm=11246000000&page=", "pages": 1},# 红桥区
        {"cate": "lmdm=010003&fjdm=11250000000&page=", "pages": 1},# 东丽区
        {"cate": "lmdm=010003&fjdm=11251000000&page=", "pages": 1},# 西青区
        {"cate": "lmdm=010003&fjdm=11252000000&page=", "pages": 1},# 津南区
        {"cate": "lmdm=010003&fjdm=11253000000&page=", "pages": 1},# 北辰区
        {"cate": "lmdm=010003&fjdm=11255000000&page=", "pages": 1},# 武清区
        {"cate": "lmdm=010003&fjdm=11257000000&page=", "pages": 1},# 宝坻区
        {"cate": "lmdm=010003&fjdm=11256000000&page=", "pages": 1},# 静海区
        {"cate": "lmdm=010003&fjdm=11254000000&page=", "pages": 1},# 宁河区
        {"cate": "lmdm=010003&fjdm=11258000000&page=", "pages": 1},# 蓟州区#6
        {"cate": "lmdm=010003&fjdm=11296000000&page=", "pages": 1},# 滨海新区
        {"cate": "lmdm=010003&fjdm=11297000000&page=", "pages": 1},# 开发区
        {"cate": "lmdm=020001&fjdm=11294000000&page=", "pages": 1},# 保税区
        {"cate": "lmdm=010003&fjdm=11298000000&page=", "pages": 1},# 高新区
        {"cate": "lmdm=010003&fjdm=11299000000&page=", "pages": 1},# 东疆港/
        {"cate": "lmdm=010003&fjdm=11248000000&page=", "pages": 1},# 中新生态城
        {"cate": "lmdm=010003&fjdm=11291000000&page=", "pages": 1},# 第三税务分局
        {"cate": "lmdm=010003&fjdm=11290000000&page=", "pages": 1},# 第四税务分局

        # 天津市
        # {"cate": "lmdm=030001&fjdm=11200000000&page=", "pages": 37},#公示37
        #
        # {"cate": "lmdm=030002&fjdm=11200000000&page=", "pages": 15},#政策解读

        # {"cate": "lmdm=030005&fjdm=11200000000&page=", "pages": 54},# 热点问答

        # {"cate": "lmdm=030006&fjdm=11200000000&page=", "pages": 14},# 税收规范性文件

        # {"cate": "lmdm=010003&fjdm=11200000000&page=", "pages": 32},# 通知公告
        # {"cate": "lmdm=01000501&fjdm=11200000000&page=", "pages": 20},# 采购信息公告

        #各个区
        # {"cate": "lmdm=010003&fjdm=11241000000&page=", "pages": 6},# 和平区6
        # {"cate": "lmdm=010003&fjdm=11242000000&page=", "pages": 7},# 河东区
        # {"cate": "lmdm=010003&fjdm=11243000000&page=", "pages": 7},# 河西区/
        # {"cate": "lmdm=010003&fjdm=11244000000&page=", "pages": 6},# 南开区
        # {"cate": "lmdm=010003&fjdm=11245000000&page=", "pages": 8},# 河北区
        # {"cate": "lmdm=010003&fjdm=11246000000&page=", "pages": 7},# 红桥区
        # {"cate": "lmdm=010003&fjdm=11250000000&page=", "pages": 9},# 东丽区
        # {"cate": "lmdm=010003&fjdm=11251000000&page=", "pages": 7},# 西青区
        # {"cate": "lmdm=010003&fjdm=11252000000&page=", "pages": 6},# 津南区
        # {"cate": "lmdm=010003&fjdm=11253000000&page=", "pages": 20},# 北辰区
        # {"cate": "lmdm=010003&fjdm=11255000000&page=", "pages": 7},# 武清区
        # {"cate": "lmdm=010003&fjdm=11257000000&page=", "pages": 6},# 宝坻区
        # {"cate": "lmdm=010003&fjdm=11256000000&page=", "pages": 6},# 静海区
        # {"cate": "lmdm=010003&fjdm=11254000000&page=", "pages": 7},# 宁河区
        # {"cate": "lmdm=010003&fjdm=11258000000&page=", "pages": 6},# 蓟州区#6
        # {"cate": "lmdm=010003&fjdm=11296000000&page=", "pages": 8},# 滨海新区
        # {"cate": "lmdm=010003&fjdm=11297000000&page=", "pages": 10},# 开发区
        # {"cate": "lmdm=020001&fjdm=11294000000&page=", "pages": 9},# 保税区
        # {"cate": "lmdm=010003&fjdm=11298000000&page=", "pages": 7},# 高新区
        # {"cate": "lmdm=010003&fjdm=11299000000&page=", "pages": 7},# 东疆港/
        # {"cate": "lmdm=010003&fjdm=11248000000&page=", "pages": 6},# 中新生态城
        # {"cate": "lmdm=010003&fjdm=11291000000&page=", "pages": 6},# 第三税务分局
        # {"cate": "lmdm=010003&fjdm=11290000000&page=", "pages": 5},# 第四税务分局



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







