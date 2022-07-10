# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class GansuxinwenItem(scrapy.Item):
    # define the fields for your item here like:
    uid = scrapy.Field()
    link = scrapy.Field()
    title = scrapy.Field()
    province = scrapy.Field()
    publish_time = scrapy.Field()
    create_time = scrapy.Field()
    author = scrapy.Field()
    countent = scrapy.Field()
    data_source = scrapy.Field()
    status = scrapy.Field()
    base = scrapy.Field()
    # pass
