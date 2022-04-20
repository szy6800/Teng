# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from twisted.enterprise import adbapi
from pymysql.converters import escape_string
import pymysql

# 列表页数据入库
class QhHousePipeline:
    def __init__(self, pool):
        self.dbpool = pool
        # 定义查询语句
        # self.update_sql3 = """UPDATE zhaobiao2021_copy1 SET province='{}';"""

        self.insert_sql = """
             INSERT INTO qh_house(
                             check_md5,url,name,house_type,area_range,nsale_time,address,features,price,lastmodifydate,detail_id,lng,lat,developers,disrictname,
                             units,housecnt,availablecnt,soldcnt,unavailablecnt,signcnt,salesname
                         )VALUES ('{}','{}', '{}', '{}', '{}', '{}', '{}', '{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')
         """
        # self.query_sql = """SELECT * FROM xian_village_quchong WHERE url_md5='{}'"""
        self.query_sql = """SELECT * FROM qh_house WHERE check_md5='{}'"""
        # 更改语句,插入语句"
        self.update_sql3 = """UPDATE qh_house SET lng='{}',lat='{}',developers='{}',disrictname='{}',units='{}',housecnt='{}',availablecnt='{}',unavailablecnt='{}',soldcnt='{}',salesname='{}' WHERE check_md5='{}';"""


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
        cursor.execute(self.query_sql.format(item['check_md5']))

        # 查看这个数据是否存在,不存在就插入
        if cursor.fetchone():
            print(f"标题 {item['name']} ==== {item['check_md5']} 已存在！！！")
        else:
            cursor.execute(self.insert_sql.format(
                # item['id'],
                item['check_md5'],
                item['url'],
                item['name'],
                item['house_type'],
                item['area_range'],
                item['nsale_time'],
                item['address'],
                item['features'],
                item['price'],
                item['lastmodifydate'],
                item['detail_id'],
                item['lng'],
                item['lat'],
                item['developers'],
                item['disrictname'],
                item['units'],
                item['housecnt'],
                item['availablecnt'],
                item['soldcnt'],
                item['unavailablecnt'],
                item['signcnt'],
                item['salesname'],
            ))
            # cursor.execute(self.qcinsert_sql.format(
            #     item['url_md5'],
            # ))
            print(f"新增房屋==== {item['check_md5']} ======{item['name']}")

#插入语句更新
    # def update(self, cursor, item):
    #     # 唯一id查询
    #
    #     cursor.execute(self.update_sql3.format(
    #         item['lng'],
    #         item['lat'],
    #         item['developers'],
    #         item['disrictname'],
    #         item['units'],
    #         item['housecnt'],
    #         item['soldcnt'],
    #         item['unavailablecnt'],
    #         item['signcnt'],
    #         item['salesname'],
    #         item['check_md5'],
    #
    #     ))
    #     print(f"更新房屋id {item['check_md5']}")


class QhbuildingPipeline:
    def __init__(self, pool):
        self.dbpool = pool
        # 定义查询语句
        # self.update_sql3 = """UPDATE zhaobiao2021_copy1 SET province='{}';"""

        self.insert_sql = """
             INSERT INTO qh_house_build(
                             check_md5,url,uid,buildno,buildid,unit,housecnt,availablecnt,soldcnt,unavailablecnt,signcnt,housename,businessvaule,price,housetype,houseconstruct,
                             buildarea,publicarea,designusage,certno,description,flooron
                         )VALUES ('{}','{}', '{}', '{}', '{}', '{}', '{}', '{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')
         """
        # self.query_sql = """SELECT * FROM xian_village_quchong WHERE url_md5='{}'"""
        self.query_sql = """SELECT * FROM qh_house_build WHERE uid='{}'"""
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
            print(f"标题 {item['buildno']} ==== {item['uid']} 已存在！！！")
        else:
            cursor.execute(self.insert_sql.format(
                # item['id'],
                item['check_md5'],
                item['url'],
                item['uid'],
                item['buildno'],
                item['buildid'],
                item['unit'],
                item['housecnt'],
                item['availablecnt'],
                item['soldcnt'],
                item['unavailablecnt'],
                item['signcnt'],
                item['housename'],
                item['businessvaule'],
                item['price'],
                item['housetype'],
                item['houseconstruct'],
                item['buildarea'],
                item['publicarea'],
                item['designusage'],
                item['certno'],
                item['description'],
                item['flooron'],


            ))
            # cursor.execute(self.qcinsert_sql.format(
            #     item['url_md5'],
            # ))
            print(f"新增房屋==== {item['uid']} ======{item['buildno']}")