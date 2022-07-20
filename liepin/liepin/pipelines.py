# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

from liepin.items import LiepinJOBItem
from liepin.items import LiepinCompItem


class LiepinPipeline:
    def process_item(self, item, spider):
        if isinstance(item, LiepinCompItem):
            print(item)

