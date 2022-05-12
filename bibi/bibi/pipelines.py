# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from itemadapter import ItemAdapter
from twisted.enterprise import adbapi
from pymysql.converters import escape_string
import pymysql
import gne

class BibiPipeline:
    def __init__(self, pool):
        self.dbpool = pool
        # 定义查询语句
        # self.update_sql3 = """UPDATE zhaobiao2021_copy1 SET province='{}';"""

        self.insert_sql = """
              INSERT INTO zb_bibi_2021_1(
                              id,code,projectName,publishDate,dataTypeStr,prov_name
                          )VALUES ('{}','{}', '{}', '{}', '{}', '{}')
          """
        # self.query_sql = """SELECT * FROM xian_village_quchong WHERE url_md5='{}'"""
        self.query_sql = """SELECT * FROM zb_bibi_2021_1 WHERE id='{}'"""
        # 更改语句,插入语句
        # self.qcinsert_sql = """
        #                INSERT INTO zb_bibi_2021_1_copy1(url_md5)VALUES ('{}')
        #            """

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
        cursor.execute(self.query_sql.format(item['id']))
        # 执行sql语句
        # cursor.execute(self.query_sql.format(item['url_md5']))
        # 查看这个数据是否存在,不存在就插入
        if cursor.fetchone():
            print(f"标题 {item['projectName']} ==== {item['id']} 已存在！！！")
        else:
            cursor.execute(self.insert_sql.format(
                item['id'],
                item['code'],
                item['projectName'],
                item['publishDate'],
                item['dataTypeStr'],
                item['prov_name'],

            ))
            # cursor.execute(self.qcinsert_sql.format(
            #     item['url_md5'],
            # ))
            print(f"新增招标==== {item['projectName']}")

