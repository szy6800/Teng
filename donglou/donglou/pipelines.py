# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface

import pymysql
from twisted.enterprise import adbapi
from pymysql.converters import escape_string  # pymsql1.0版本以上用pymysql.converters


class DonglouPipeline(object):
    def __init__(self, pool):
        self.dbpool = pool
        # 定义查询语句
        # self.query_sql = """SELECT * FROM arch_info_crawler_copy1 WHERE arch_id='{}'"""
        # 更改语句,插入语句
        # self.insert_sql = """
        #     INSERT INTO arch_info_crawler(
        #                     arch_id, prov_name, city_name, country_name, arch_name, link ,arch_add, avg_price, dispx, dispy, build_category,
        #                     property_fee, property_company, building_developers,building_number,source_name,crawler_time,house_number
        #                 )VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}','{}',
        #                 '{}', '{}', '{}', '{}', '{}')
        # """
        #
        self.update_sql3 = """UPDATE arch_info_crawler_copy1 SET dispx='{}', dispy='{}' WHERE arch_id='{}';"""

    @classmethod
    def from_settings(cls, settings):
        params = dict(
            host=settings['MYSQL_HOST'],
            port=settings['MYSQL_PORT'],
            db=settings['MYSQL_DB'],
            user=settings['MYSQL_USER'],
            passwd=settings['MYSQL_PASSWD'],
            charset=settings['MYSQL_CHARSET'],
            cursorclass=pymysql.cursors.DictCursor
        )
        db_connect_pool = adbapi.ConnectionPool('pymysql', **params)
        obj = cls(db_connect_pool)
        return obj

    def process_item(self, item, spider):
        result = self.dbpool.runInteraction(self.insert, item)
        # result.addErrback(self.error)

    def error(self, reason):
        print('error------', reason)

    def insert(self, cursor, item):
        # 唯一id查询
        try:
            cursor.execute(self.update_sql3.format(
                item['dispx'],
                item['dispy'],
                item['arch_id'],
            ))
            print(f"更新楼盘 {item['arch_id']}")
        except:
            print(item['arch_id'])
        # cursor.execute(self.query_sql.format(item['arch_id']))
        # # cursor.execute(self.update_sql3.format(item['dispx'],item['dispy'],item['arch_id']))
        # if cursor.fetchone():
        #     print(f"新房 {item['arch_name']} ==== {item['arch_id']} 已存在！！！")
        # else:
        #     cursor.execute(self.insert_sql.format(
        #         item['arch_id'],
        #         item['prov_name'],
        #         item['city_name'],
        #         item['country_name'],
        #         item['arch_name'],
        #         item['link'],
        #         item['arch_add'],
        #         item['avg_price'],
        #         item['dispx'],
        #         item['dispy'],
        #         item['build_category'],
        #         item['property_fee'],
        #         item['property_company'],
        #         item['building_developers'],
        #         item['building_number'],
        #         item['source_name'],
        #         item['crawler_time'],
        #         item['house_number']
        #     ))
        #     print(f"新增楼盘==== {item['arch_id']} ======{item['arch_name']}")
