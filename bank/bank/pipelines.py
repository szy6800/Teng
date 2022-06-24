# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymysql
from twisted.enterprise import adbapi
from pymysql.converters import escape_string
from bank import settings

class BankPipeline:
    def __init__(self, pool):
        self.dbpool = pool
        # 更改语句,插入语句
        self.insert_sql = """
            INSERT INTO bank2_copy1_copy1(
                        certCode, dates, setDate, fullName, flowNo,type,useState,endDate
                        )VALUES ('{}','{}', '{}', '{}', '{}', '{}', '{}','{}')
        """
      # 定义查询语句
        self.query_sql = """SELECT * FROM bank2_copy1_copy1 WHERE certCode='{}'"""

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
        cursor.execute(self.query_sql.format(item['certCode']))
        if cursor.fetchone():
            print(f"标题 {item['certCode']} ==== 已存在！！！")
        else:
            cursor.execute(self.insert_sql.format(
                # item['id'],
                item['certCode'],
                item['dates'],
                item['setDate'],
                item['fullName'],
                item['flowNo'],
                item['type'],
                item['useState'],
                item['endDate'],
            ))
            print(f"新增公告==== {item['flowNo']} ======{item['fullName']}")
