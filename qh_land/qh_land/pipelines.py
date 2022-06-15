# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

from twisted.enterprise import adbapi
from pymysql.converters import escape_string
import pymysql


class QhLandPipeline:
    def __init__(self, pool):
        self.dbpool = pool
        # 定义查询语句
        # self.update_sql3 = """UPDATE zhaobiao2021_copy1 SET province='{}';"""

        self.insert_sql = """
             INSERT INTO qh_land(
                             uid,detail_id,district,address,url,area,land_use ,supply_mode,sign_date,
                             province,city,county,ele_num,pro_name,land_source,ser_life,industry,land_level,tran_price,app_unit,app_num
                         )VALUES ('{}','{}', '{}', '{}', '{}', '{}', '{}', '{}','{}','{}','{}','{}','{}'
                         ,'{}','{}','{}','{}','{}','{}','{}','{}')
         """
        # self.query_sql = """SELECT * FROM xian_village_quchong WHERE url_md5='{}'"""
        self.query_sql = """SELECT * FROM qh_land WHERE uid='{}'"""
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
            print(f"标题 {item['pro_name']} ==== {item['uid']} 已存在！！！")
        else:
            cursor.execute(self.insert_sql.format(
                # item['id'],
                item['uid'],
                item['detail_id'],
                item['district'],
                item['address'],
                item['url'],
                item['area'],
                item['land_use'],
                item['supply_mode'],
                item['sign_date'],
                item['province'],
                item['city'],
                item['county'],
                item['ele_num'],
                item['pro_name'],
                item['land_source'],
                item['ser_life'],
                item['industry'],
                item['land_level'],
                item['tran_price'],
                item['app_unit'],
                item['app_num'],

            ))
            # cursor.execute(self.qcinsert_sql.format(
            #     item['url_md5'],
            # ))
            print(f"新增房屋==== {item['uid']} ======{item['pro_name']}")
