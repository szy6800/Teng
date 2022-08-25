# -*- coding: utf-8 -*-
def process(text):
    """Version:
    来源提取
    """
    import re
    # 按需排序
    rules = [
        # r"([\u4e00-\u9fa5]+)",  # 默认提取中文, 其它格式卡住后处理
        r".*",  # 默认提取中文, 其它格式卡住后处理
        # r"", # 自定义
        # r"([^\s/$.?].[^\s]*)", # www.railwaygazette.com
    ]
    # 预处理，替换掉会影响正则提取的固定字符串, 从验证器中更新
    flags = ["公司地址：","所属行业：","成立时间：",""]
    for each in flags:
        text = text.replace(each, "")
    # 来源为空
    if len(re.sub(r"\s+", "", text)) < 1:
        return ""
    # 提取来源
    for each in rules:
        p = re.compile(each)
        res = p.findall(text)
        if res:
            res = sorted(res, key=len, reverse=True)
            return res[0]
        else:
            continue
    else:
        return f"error:[{text}]"


