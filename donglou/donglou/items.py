# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class DonglouItem(scrapy.Item):
    # define the fields for your item here like:
    arch_id = scrapy.Field()
    prov_name = scrapy.Field()
    city_name = scrapy.Field()
    country_name = scrapy.Field()
    arch_name = scrapy.Field()
    link = scrapy.Field()
    arch_add = scrapy.Field()
    avg_price = scrapy.Field()
    dispx = scrapy.Field()
    dispy = scrapy.Field()
    build_category = scrapy.Field()
    property_fee = scrapy.Field()
    property_company = scrapy.Field()
    building_developers = scrapy.Field()
    building_number = scrapy.Field()
    source_name = scrapy.Field()
    crawler_time = scrapy.Field()
    house_number = scrapy.Field()

