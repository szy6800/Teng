# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy import *


class QinghaiItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    uid = Field()  # id
    uuid = Field()  # (可无)
    title = Field()  # 标题
    link = Field()  # url
    intro = Field()  # 前言
    abs = Field()  # abs
    content = Field()  # 内容html/json
    publish_time = Field()  # 发布时间
    purchaser = Field()  # 购买方
    proxy = Field()  # 代理人
    create_time = Field()  # 创建时间
    update_time = Field()  # 更新时间
    deleted = Field()  # 是否删除
    province = Field()  # 省份/地域
    base = Field()  # 基础
    type = Field()  # 类型
    items = Field()  # 行业
    data_source = Field()  # 类型编号
    end_time = Field()  # 报价截止时间
    status = Field()  # 状态
    serial = Field()  # 采购编号
