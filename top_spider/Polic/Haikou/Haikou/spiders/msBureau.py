# 人民政府
def indexGov():
    ##['http://www.haikou.gov.cn/xxgk/szfbjxxgk/ggtz/index.html']
    ## http://www.haikou.gov.cn/xxgk/szfbjxxgk/zcfg/dfxfg/index.html
    ## http://www.haikou.gov.cn/xxgk/szfbjxxgk/zcfg/szfxzgfxwj/index.html
    ## http://www.haikou.gov.cn/xxgk/szfbjxxgk/zcfg/bmxzgfxwj/index.html
    ## http://www.haikou.gov.cn/xxgk/szfbjxxgk/zcjd/zxjd/index_8.html
    cates = [
        {"cate": "ggtz/", "pages": 1},  # >公示公告 99
        {"cate": "zcfg/dfxfg/", "pages": 1},  # >地方性法规 5
        {"cate": "zcfg/szfxzgfxwj/", "pages": 1},  # >市政府行政规范性文件 5
        {"cate": "zcfg/bmxzgfxwj/", "pages": 1},  # >部门行政规范性文件 3
        {"cate": "zcjd/zxjd/", "pages": 1},  # >解读 8
    ]
    return cates


# 市场监督管理局
def indexMarket():
    cates = [
        {"cate": "xxgk/gsgg/", "pages": 1},  # 通知公告 10
        {"cate": "xxgk/zcwj/flfg/", "pages": 1},  # 政策文件 2
        {"cate": "jdhy/zxjd/", "pages": 1},  # 解读  1
    ]
    return cates


# 人力资源和社会保障局
# http://rsj.haikou.gov.cn/xxgk/gsgg/index.html #公示公告 49
# http://rsj.haikou.gov.cn/xxgk/zcfg/bmzcwj/index.html  #政策部门文件 5
# http://rsj.haikou.gov.cn/jdhy/zxjd/index.html  #解读 1
def indexHuman():
    cates = [
        {"cate": "xxgk/gsgg/", "pages": 1},#公示公告 49
        {"cate": "xxgk/zcfg/bmzcwj/", "pages": 1},
        {"cate": "jdhy/zxjd/", "pages": 1},
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


def method_name(response):
    attachment_name = response.xpath(
        '//*[(contains(translate(@href, "PDF", "pdf"), ".pdf") or contains(translate(@href, "XLS", "xls"), ".xls")'
        ' or contains(translate(@href, "DOC", "doc"), ".doc") or contains(translate(@href, "ZIP", "zip"), ".zip")'
        ' or contains(translate(@href, "RAR", "rar"), ".rar") or contains(translate(@href, "WPS", "wps"), ".wps"))'
        ' and not(contains(@href, "file://") or contains(@href, "c:\") or contains(@href, "c:\"))]//text() |'
        ' .//*[contains(translate(@src, "MP4","mp4"), ".mp4") and not(contains(@src, "file://") or'
        ' contains(@src,"c:\") or contains(@src, "C:\"))]//text()').getall()
    return attachment_name


def methodNameUrl(response):
    return response.xpath(
        '//*[(contains(translate(@href, "PDF", "pdf"), ".pdf") or contains(translate(@href, "XLS", "xls"), ".xls") or contains(translate(@href, "DOC", "doc"), ".doc") or contains(translate(@href, "ZIP", "zip"), ".zip") or contains(translate(@href, "RAR", "rar"), ".rar") or contains(translate(@href, "WPS", "wps"), ".wps")) and not(contains(@href, "file://") or contains(@href, "c:\") or contains(@href, "c:\"))]/@href | .//*[contains(translate(@src, "MP4","mp4"), ".mp4") and not(contains(@src, "file://") or contains(@src,"c:\") or contains(@src, "C:\"))]/@src').getall()
