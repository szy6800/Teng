# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

# useful for handling different item types with a single interface

from liepin.items import LiepinJOBItem
from liepin.items import LiepinCompItem
import pymysql
from twisted.enterprise import adbapi
from pymysql.converters import escape_string


class LiepinPipeline:
    def __init__(self, pool):
        self.dbpool = pool
        # 查询语句
        self.query_sql = """SELECT * FROM comquchong WHERE cid='{}'"""
        # 更改语句,插入语句
        self.qcinsert_sql = """
                            INSERT INTO comquchong(cid)VALUES ('{}')
                        """
        self.job_insert_sql = """
            INSERT INTO jobs(
                            uid, link, job_title, job_indu, salary, work_years, job_tags,
                            city, job_desc, education, comp_name,cid,source,base,pub_time
                        )VALUES ('{}','{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}','{}','{}','{}','{}')
        """

        self.com_insert_sql = """
             INSERT INTO company(
                             cid, link, name, comp_ind, num_of_peo, fig_stage, comp_addr,
                             reg_time, reg_capi, op_period, man_range,comp_desc,lng,lat,logo,welfare,legal_peo,reg_au,comp_code,
                             status,comp_link,locations,comp_type,comp_website
                         )VALUES ('{}','{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')
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
        self.result = self.dbpool.runInteraction(self.insert, item)

    def error(self, reason):
        print('error------', reason)

    def insert(self, cursor, item):
        if len(item) == 15:
            cursor.execute(self.job_insert_sql.format(
                item['uid'],
                item['link'],
                item['job_title'],
                item['job_indu'],
                item['salary'],
                item['work_years'],
                item['job_tags'],
                item['city'],
                escape_string(item['job_desc']),
                item['education'],
                item['comp_name'],
                item['cid'],
                item['source'],
                item['base'],
                item['pub_time'],
            ))
            print(f"新增岗位==== {item['uid']} ======{item['job_title']}")
        else:
            cursor.execute(self.query_sql.format(item['cid']))
            if cursor.fetchone():
                print(f"公司 {item['name']} ==== {item['cid']} 已存在！！！")
            else:
                cursor.execute(self.qcinsert_sql.format(
                    item['cid']
                ))
                cursor.execute(self.com_insert_sql.format(
                    item['cid'],
                    item['link'],
                    item['name'],
                    item['comp_ind'],
                    item['num_of_peo'],
                    item['fig_stage'],
                    item['comp_addr'],
                    item['reg_time'],
                    item['reg_capi'],
                    item['op_period'],
                    item['man_range'],
                    escape_string(item['comp_desc']),
                    item['lng'],
                    item['lat'],
                    item['logo'],
                    item['welfare'],
                    item['legal_peo'],
                    item['reg_au'],
                    item['comp_code'],
                    item['status'],
                    item['comp_link'],
                    item['locations'],
                    item['comp_type'],
                    item['comp_website'],
                ))
                print(f"新增公司==== {item['cid']} ======{item['name']}")


