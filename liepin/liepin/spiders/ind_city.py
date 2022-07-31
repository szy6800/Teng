# -*- coding: utf-8 -*-
# 行业列表
import requests
import json


def index():
    url = 'https://apic.liepin.com/api/com.liepin.searchfront4c.pc-search-condition-list'
    res = requests.get(url).json()
    # 获取行业json列表
    ls = res['data']['industryCondition']
    # 准备一个列表放进去
    ind = []
    for i in ls:
        ls1 = i['children']
        for i1 in ls1:
            ls2 = dict()
            # 大分类
            ls2['big_type'] = i['name']
            # 小分类
            ls2['small_type'] = i1['name']
            # 编码
            ls2['code'] = i1['code']
            ind.append(ls2)
    print(ind)


def ind():
    ind_list = [{'big_type': '互联网.游戏.软件', 'small_type': '互联网/电商', 'code': '040'}, {'big_type': '互联网.游戏.软件', 'small_type': '游戏产业', 'code': '420'}, {'big_type': '互联网.游戏.软件', 'small_type': '计算机软件', 'code': '010'}, {'big_type': '互联网.游戏.软件', 'small_type': 'IT服务', 'code': '030'}, {'big_type': '电子.通信.硬件', 'small_type': '电子/芯片/半导体', 'code': '050'}, {'big_type': '电子.通信.硬件', 'small_type': '通信业', 'code': '060'}, {'big_type': '电子.通信.硬件', 'small_type': '计算机/网络设备', 'code': '020'}, {'big_type': '房地产.建筑.物业', 'small_type': '房地产/建筑', 'code': '080'}, {'big_type': '房地产.建筑.物业', 'small_type': '房地产服务', 'code': '090'}, {'big_type': '房地产.建筑.物业', 'small_type': '规划/设计/装潢', 'code': '100'}, {'big_type': '金融', 'small_type': '银行', 'code': '130'}, {'big_type': '金融', 'small_type': '保险', 'code': '140'}, {'big_type': '金融', 'small_type': '基金/证券/投资', 'code': '150'}, {'big_type': '金融', 'small_type': '会计/审计', 'code': '430'}, {'big_type': '金融', 'small_type': '信托/担保/拍卖', 'code': '500'}, {'big_type': '消费品', 'small_type': '食品/饮料/日化', 'code': '190'}, {'big_type': '消费品', 'small_type': '批发零售', 'code': '240'}, {'big_type': '消费品', 'small_type': '服装纺织', 'code': '200'}, {'big_type': '消费品', 'small_type': '家具/家电', 'code': '210'}, {'big_type': '消费品', 'small_type': '办公设备', 'code': '220'}, {'big_type': '消费品', 'small_type': '奢侈品/收藏品', 'code': '460'}, {'big_type': '消费品', 'small_type': '珠宝/玩具/工艺品', 'code': '470'}, {'big_type': '汽车.机械.制造', 'small_type': '汽车/摩托车', 'code': '350'}, {'big_type': '汽车.机械.制造', 'small_type': '机械/机电/重工', 'code': '360'}, {'big_type': '汽车.机械.制造', 'small_type': '印刷/包装/造纸', 'code': '180'}, {'big_type': '汽车.机械.制造', 'small_type': '仪器/电气/自动化', 'code': '340'}, {'big_type': '汽车.机械.制造', 'small_type': '原材料加工', 'code': '370'}, {'big_type': '服务.外包.中介', 'small_type': '中介服务', 'code': '110'}, {'big_type': '服务.外包.中介', 'small_type': '专业服务', 'code': '120'}, {'big_type': '服务.外包.中介', 'small_type': '外包服务', 'code': '440'}, {'big_type': '服务.外包.中介', 'small_type': '检测/认证', 'code': '450'}, {'big_type': '服务.外包.中介', 'small_type': '餐饮/酒旅/服务', 'code': '230'}, {'big_type': '服务.外包.中介', 'small_type': '租赁服务', 'code': '510'}, {'big_type': '广告.传媒.教育.文化', 'small_type': '文体娱乐', 'code': '260'}, {'big_type': '广告.传媒.教育.文化', 'small_type': '广告/市场/会展', 'code': '070'}, {'big_type': '广告.传媒.教育.文化', 'small_type': '影视文化', 'code': '170'}, {'big_type': '广告.传媒.教育.文化', 'small_type': '教育培训', 'code': '380'}, {'big_type': '交通.贸易.物流', 'small_type': '交通/物流/运输', 'code': '250'}, {'big_type': '交通.贸易.物流', 'small_type': '贸易/进出口', 'code': '160'}, {'big_type': '交通.贸易.物流', 'small_type': '航空/航天', 'code': '480'}, {'big_type': '制药.医疗', 'small_type': '制药/生物工程', 'code': '270'}, {'big_type': '制药.医疗', 'small_type': '医疗/保健/美容', 'code': '280'}, {'big_type': '制药.医疗', 'small_type': '医疗器械', 'code': '290'}, {'big_type': '能源.化工.环保', 'small_type': '环保', 'code': '300'}, {'big_type': '能源.化工.环保', 'small_type': '石油/化工', 'code': '310'}, {'big_type': '能源.化工.环保', 'small_type': '采掘/冶炼/矿产', 'code': '320'}, {'big_type': '能源.化工.环保', 'small_type': '能源/水利', 'code': '330'}, {'big_type': '能源.化工.环保', 'small_type': '新能源', 'code': '490'}, {'big_type': '政府.农林牧渔', 'small_type': '政务/公共服务', 'code': '390'}, {'big_type': '政府.农林牧渔', 'small_type': '农林牧渔', 'code': '410'}, {'big_type': '政府.农林牧渔', 'small_type': '其他行业', 'code': '400'}]
    return ind_list



