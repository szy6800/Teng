# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import pymysql
from twisted.enterprise import adbapi
from pymysql.converters import escape_string # pymsql1.0版本以上用pymysql.converters

class LoupanFPipeline(object):
    def __init__(self, pool):
        self.dbpool = pool
        # 定义查询语句
        self.query_sql = """SELECT * FROM ftx_maindoor WHERE uid='{}'"""
        self.query_sql1 = """SELECT * FROM ftx_buliding WHERE quchong='{}'"""
        # 更改语句,插入语句
        self.insert_sql = """
            INSERT INTO ftx_maindoor(
                            uid, main, forsale
                        )VALUES ('{}', '{}', '{}')
        """

        self.insert_sql1 = """
                    INSERT INTO ftx_buliding(
                                    uid, quchong, domain, building, element, elevator, floor, households
                                )VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')
                """

        self.update_sql2 = """UPDATE crawler2021.arch_info_crawler SET archend_time='{}' WHERE uid='{}';"""

        self.update_sql4 = """UPDATE crawler2021.arch_info_crawler SET Decorate_state='{}' WHERE uid='{}';"""

        self.update_sql3 = """UPDATE test.arch_info_price SET dispx='{}', dispy='{}' WHERE uid='{}';"""


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
        # # 唯一id查询
        # cursor.execute(self.query_sql.format(item['uid']))
        # # cursor.execute(self.query_sql1.format(item['quchong']))
        # if cursor.fetchone():
        #     print(f"户型 {item['main']} ==== {item['uid']} 已存在！！！")
        #     # print(f"户型 {item['domain']} ==== {item['quchong']} 已存在！！！")
        # else:
        #     cursor.execute(self.insert_sql.format(
        #         item['uid'],
        #         item['main'],
        #         item['forsale']
        #     ))
        #     print(f"新增户型==== {item['uid']} ======{item['main']}")
        # uid, quchong, domain, buildin, element, elevator, floor, households
        # cursor.execute(self.insert_sql1.format(
        #     item['uid'],
        #     item['quchong'],
        #     item['domain'],
        #     item['building'],
        #     item['element'],
        #     item['elevator'],
        #     item['floor'],
        #     item['households']
        # ))
        # print(f"新增栋楼==== {item['quchong']} ======{item['domain']}")

        # try:
        #     cursor.execute(self.update_sql2.format(
        #         item['archend_time'],
        #         item['uid']
        #     ))
        #     print(f"更新楼盘 {item['uid']}")
        # except:
        #     print(item['uid'])

        try:
            cursor.execute(self.update_sql4.format(
                item['Decorate_state'],
                item['uid']
            ))
            print(f"更新楼盘 {item['uid']}")
        except:
            print(item['uid'])


        # try:
        #     cursor.execute(self.update_sql3.format(
        #         item['dispx'],
        #         item['dispy'],
        #         item['uid']
        #     ))
        #     print(f"更新楼盘 {item['uid']}")
        # except:
        #     print(item['uid'])
        #


