# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from twisted.enterprise import adbapi
from pymysql.converters import escape_string
import pymysql


class BossPipeline:
    def __init__(self, pool):
        self.dbpool = pool
        # 定义查询语句
        # self.update_sql3 = """UPDATE zhaobiao2021_copy1 SET province='{}';"""

        self.insert_sql = """
             INSERT INTO job_type(
                             big_type,big_code,mid_type,mid_code,small_type,small_code
                         )VALUES ('{}','{}', '{}', '{}', '{}', '{}')
         """
        # self.query_sql = """SELECT * FROM xian_village_quchong WHERE url_md5='{}'"""
        self.query_sql = """SELECT * FROM job_type WHERE small_code='{}'"""
        # 更改语句,插入语句"
        #self.update_sql3 = """UPDATE qh_house SET lng='{}',lat='{}',developers='{}',disrictname='{}',units='{}',housecnt='{}',availablecnt='{}',unavailablecnt='{}',soldcnt='{}',salesname='{}' WHERE check_md5='{}';"""


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
        # print(item)

        result = self.dbpool.runInteraction(self.insert, item)
        # print(item)
        # 插入语句
        # result = self.dbpool.runInteraction(self.update, item)
        # result.addErrback(self.error)

    def insert(self, cursor, item):

        print(item)
        #唯一id查询 执行sql语句
        # cursor.execute(self.query_sql.format(item['small_code']))
        # # 查看这个数据是否存在,不存在就插入
        # if cursor.fetchone():
        #     print(f"标题 {item['small_type']} ==== {item['small_code']} 已存在！！！")
        # else:
        #     cursor.execute(self.insert_sql.format(
        #         # item['id'],
        #         item['big_type'],
        #         item['big_code'],
        #         item['mid_type'],
        #         item['mid_code'],
        #         item['small_type'],
        #         item['small_code'],
        #
        #     ))
        #
        #     print(f"新增==== {item['small_type']} ======{item['small_code']}")
