# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
# from itemadapter import ItemAdapter

from twisted.enterprise import adbapi
from pymysql.converters import escape_string
import pymysql


class ParkPipeline:
    def __init__(self, pool):
        self.dbpool = pool
        # 定义查询语句
        # self.update_sql3 = """UPDATE zhaobiao2021_copy1 SET province='{}';"""

        self.insert_sql = """
             INSERT INTO ind_park(
                             title,uid,link,industry,purchase,province,city,county,is_coo,
                             area,comp_num,price,address,lng,lat
                         )VALUES ('{}','{}', '{}', '{}', '{}', '{}', '{}', '{}','{}','{}','{}','{}','{}'
                         ,'{}','{}')
         """
        # self.query_sql = """SELECT * FROM xian_village_quchong WHERE url_md5='{}'"""
        self.query_sql = """SELECT uid FROM ind_park WHERE uid='{}'"""
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
        result = self.dbpool.runInteraction(self.insert, item)
        # 插入语句
        # result = self.dbpool.runInteraction(self.update, item)
        # result.addErrback(self.error)

    def error(self, reason):
        print('error------', reason)

    def insert(self, cursor, item):
        # 唯一id查询 执行sql语句
        cursor.execute(self.query_sql.format(item['uid']))
        # 查看这个数据是否存在,不存在就插入
        if cursor.fetchone():
            print(f"标题 {item['title']} ==== {item['uid']} 已存在！！！")
        else:
            cursor.execute(self.insert_sql.format(
                # item['id'],
                item['title'],
                item['uid'],
                item['link'],
                item['industry'],
                item['purchase'],
                item['province'],
                item['city'],
                item['county'],
                item['is_coo'],
                item['area'],
                item['comp_num'],
                item['price'],
                escape_string(item['address']),
                item['lng'],
                item['lat'],
            ))
            # cursor.execute(self.qcinsert_sql.format(
            #     item['url_md5'],
            # ))
            print(f"新增數據==== {item['uid']} ======{item['title']}")
