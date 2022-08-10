# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class LiepinJOBItem(scrapy.Item):
    # define the fields for your item here like:
    uid = scrapy.Field()
    link = scrapy.Field()
    job_title = scrapy.Field()
    name = scrapy.Field()
    job_indu = scrapy.Field()
    salary = scrapy.Field()
    work_years = scrapy.Field()
    job_tags = scrapy.Field()
    city  = scrapy.Field()
    job_desc = scrapy.Field()
    education = scrapy.Field()
    comp_name = scrapy.Field()
    cid = scrapy.Field()
    source = scrapy.Field()
    base = scrapy.Field()

    pub_time = scrapy.Field()


class LiepinCompItem(scrapy.Item):
    cid = scrapy.Field()
    name = scrapy.Field()
    link = scrapy.Field()
    comp_ind = scrapy.Field()
    num_of_peo = scrapy.Field()
    fig_stage = scrapy.Field()
    comp_addr = scrapy.Field()
    reg_time = scrapy.Field()
    reg_capi = scrapy.Field()
    op_period = scrapy.Field()
    man_range = scrapy.Field()
    comp_desc = scrapy.Field()
    lng = scrapy.Field()
    lat = scrapy.Field()
    logo = scrapy.Field()
    welfare = scrapy.Field()
    #更新
    legal_peo = scrapy.Field()
    reg_au = scrapy.Field()
    comp_code = scrapy.Field()
    status = scrapy.Field()
    comp_link = scrapy.Field()
    locations = scrapy.Field()
    comp_type = scrapy.Field()
    comp_website = scrapy.Field()

