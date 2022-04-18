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



class QhSchoolPipeline:
    def __init__(self, pool):
        self.dbpool = pool
        # 定义查询语句
        # self.update_sql3 = """UPDATE zhaobiao2021_copy1 SET province='{}';"""

        self.insert_sql = """
             INSERT INTO qh_project(
                             check_md5,url,num,name,type,builder,address,bui_add,leader,purpose,bui_nature,scale,
                             filing_time,code,fu_nature,bui_mode,bui_area,
                             doc_num,doc_level,check_unit,check_time,land_licence,eng_licence,total_inv,other_inv,unit_pro_num,unit_pro_name,unit_pro_type,unit_pro_bui,
                             unit_pro_str,unit_pro_che,bui_dec,bui_acc,lng,lat
                         )VALUES ('{}','{}', '{}', '{}', '{}', '{}', '{}', '{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}', 
                         '{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')
         """
        # self.query_sql = """SELECT * FROM xian_village_quchong WHERE url_md5='{}'"""
        self.query_sql = """SELECT * FROM qh_project WHERE check_md5='{}'"""
        # 更改语句,插入语句
        # self.qcinsert_sql = """
        #               INSERT INTO xian_village_quchong(url_md5)VALUES ('{}')
        #           """

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
        cursor.execute(self.query_sql.format(item['check_md5']))
        # 执行sql语句
        # cursor.execute(self.query_sql.format(item['url_md5']))
        # 查看这个数据是否存在,不存在就插入
        if cursor.fetchone():
            print(f"标题 {item['name']} ==== {item['check_md5']} 已存在！！！")
        else:
            cursor.execute(self.insert_sql.format(
                # item['id'],
                item['check_md5'],
                item['url'],
                item['num'],
                item['name'],
                item['type'],
                item['builder'],
                item['address'],
                item['bui_add'],
                item['leader'],
                item['purpose'],
                item['bui_nature'],
                item['scale'],
                item['filing_time'],
                item['code'],
                item['fu_nature'],
                item['bui_mode'],
                item['bui_area'],
                item['doc_num'],
                item['doc_level'],
                item['check_unit'],
                item['check_time'],
                item['land_licence'],
                item['eng_licence'],
                item['total_inv'],
                item['other_inv'],
                item['unit_pro_num'],
                item['unit_pro_name'],
                item['unit_pro_type'],
                item['unit_pro_bui'],
                item['unit_pro_str'],
                item['unit_pro_che'],
                item['bui_dec'],
                item['bui_acc'],
                item['lng'],
                item['lat'],
            ))
            # cursor.execute(self.qcinsert_sql.format(
            #     item['url_md5'],
            # ))
            print(f"新增工程==== {item['check_md5']} ======{item['name']}")
