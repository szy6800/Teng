
#小行业
def index():
    cates = [

                {"cate": "gdsw/gzsw_jcgg/gzsw_list_area", "pages": 1},#基层公告
                {"cate": "gdsw/gzsw_tggg/city_list", "pages": 1},#通知公告
                {"cate": "gdsw/gzsw_gkwj/city_list", "pages": 1},#最新文件
                {"cate": "gdsw/gzsw_zcjd/city_list", "pages": 1},#解读
                {"cate": "gdsw/gzsw_zfcg/city_list", "pages": 1},#政府采购
                {"cate": "gdsw/ywblzn/city_list", "pages": 1},#指南
                {"cate": "gdsw/gzsw_xzfw/city_list", "pages": 1},#政府采购

                # {"cate": "gdsw/gzsw_jcgg/gzsw_list_area", "pages": 99},#基层公告
                # {"cate": "gdsw/gzsw_tggg/city_list", "pages": 14},#通知公告
                # {"cate": "gdsw/gzsw_gkwj/city_list", "pages": 5},#最新文件
                # {"cate": "gdsw/gzsw_zcjd/city_list", "pages": 3},#解读
                # {"cate": "gdsw/gzsw_zfcg/city_list", "pages": 15},#政府采购
                # {"cate": "gdsw/ywblzn/city_list", "pages": 6},#指南
                # {"cate": "gdsw/gzsw_xzfw/city_list", "pages": 3},#政府采购

                {"cate": "gdsw/zxwj/zxwj", "pages": 1},#广东省最新文件
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








