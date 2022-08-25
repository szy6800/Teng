
#小行业
def index():
    cates = [
                #
        {"cate": "inter/xiongAnPageNews?siteIdXml=11325&&keyWord=%E9%80%9A%E7%9F%A5&pageNo=", "pages": 1},#通知 147
        {"cate": "inter/xiongAnPageNews?siteIdXml=11325&&keyWord=%E6%B3%95%E4%BA%BA%E6%9C%8D%E5%8A%A1&pageNo=", "pages": 1},#指南 25
        # {"cate": "inter/xiongAnPageNews?siteIdXml=11325&&keyWord=%E9%80%9A%E7%9F%A5&pageNo=", "pages": 147},#通知 147
        # {"cate": "inter/xiongAnPageNews?siteIdXml=11325&&keyWord=%E6%B3%95%E4%BA%BA%E6%9C%8D%E5%8A%A1&pageNo=", "pages": 25},#指南 25
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







