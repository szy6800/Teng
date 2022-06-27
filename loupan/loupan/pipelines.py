# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


import pymysql
from twisted.enterprise import adbapi
from pymysql.converters import escape_string  # pymsql1.0版本以上用pymysql.converters

class LoupanPipeline(object):
    def __init__(self, pool):
        self.dbpool = pool
        # 定义查询语句
        self.query_sql = """SELECT * FROM arch_info_crawler WHERE id='{}'"""
        # 更改语句,插入语句
        self.insert_sql = """
            INSERT INTO arch_info_crawler(
                            uid, arch_id, prov_name, city_name, country_name, arch_name, arch_add,dispx, dispy,
                            build_category,right_desc,operastion,building_developers,building_area,plot_ratio,parking_number,building_number,
                            house_number,property_company,property_fee,arch_floor,avg_price,building_time,main_door,main_door_area,
                            json_data,unit_number,verification,avg_rent,source_name,source,crawler_time,link,covers_area)VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}','{}', 
                        '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}','{}', 
                        '{}', '{}', '{}', '{}','{}','{}','{}')
        """

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
        cursor.execute(self.query_sql.format(item['arch_id']))
        if cursor.fetchone():
            print(f"新房 {item['arch_name']} ==== {item['arch_id']} 已存在！！！")
        else:
            cursor.execute(self.insert_sql.format(
                item['uid'],
                item['arch_id'],
                item['prov_name'],
                item['city_name'],
                item['country_name'],
                item['arch_name'],
                item['arch_add'],
                item['dispx'],
                item['dispy'],
                item['build_category'],
                item['right_desc'],
                item['operastion'],
                item['building_developers'],
                item['building_area'],
                item['plot_ratio'],
                item['parking_number'],
                item['building_number'],
                item['house_number'],
                item['property_company'],
                item['property_fee'],
                item['arch_floor'],
                item['avg_price'],
                item['building_time'],
                item['main_door'],
                item['main_door_area'],
                item['json_data'],
                item['unit_number'],
                item['verification'],
                item['avg_rent'],
                # item['update'],
                item['source_name'],
                item['source'],
                item['crawler_time'],
                item['link'],
                item['covers_area']
            ))
            print(f"新增楼盘==== {item['arch_id']} ======{item['arch_name']}")



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
        self.update_sql3 = """UPDATE ershou SET esf_count='{}', price='{}' WHERE id='{}';"""

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
                item['esf_count'],
                item['price'],
                item['id'],
            ))
            print(f"更新楼盘 {item['id']}")
        except:
            print(item['id'])