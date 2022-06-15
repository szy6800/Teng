# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
from twisted.enterprise import adbapi
from pymysql.converters import escape_string


class QinghaiPipeline(object):
    def __init__(self, pool):
        self.dbpool = pool
        # 定义查询语句
        self.query_sql = """SELECT * FROM zhaobiaoquchong WHERE uid='{}'"""
        # 更改语句,插入语句
        self.qcinsert_sql = """
                    INSERT INTO zhaobiaoquchong(uid)VALUES ('{}')
                """
        self.insert_sql = """
            INSERT INTO zhaobiao2021(
                            uid, uuid, title, link, intro,abs, content,publish_time,purchaser,proxy,create_time,
                            update_time,deleted,province,base,type,items,data_source,end_time,status,serial
                        )VALUES ('{}','{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}','{}', 
                        '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')
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
        cursor.execute(self.query_sql.format(item['uid']))
        if cursor.fetchone():
            print(f"标题 {item['title']} ==== {item['uid']} 已存在！！！")
        else:
            cursor.execute(self.qcinsert_sql.format(
                item['uid']
            ))
            cursor.execute(self.insert_sql.format(
                # item['id'],
                item['uid'],
                item['uuid'],
                item['title'],
                item['link'],
                item['intro'],
                item['abs'],
                # 转义符
                escape_string(item['content']),
                # item['content'],
                item['publish_time'],
                item['purchaser'],
                item['proxy'],
                item['create_time'],
                item['update_time'],
                item['deleted'],
                item['province'],
                item['base'],
                item['type'],
                item['items'],
                item['data_source'],
                item['end_time'],
                item['status'],
                item['serial']
            ))
            print(f"新增公告==== {item['uid']} ======{item['title']}")




class YushouPipeline(object):
    def __init__(self, pool):
        self.dbpool = pool
        # 定义查询语句
        self.query_sql = """SELECT * FROM zhaobiao2021 WHERE uid='{}'"""
        # 更改语句,插入语句
        self.insert_sql = """
            INSERT INTO zhaobiao2021(
                            uid, uuid, title, link, intro,abs, content,publish_time,purchaser,proxy,create_time,
                            update_time,deleted,province,base,type,items,data_source,end_time,status,serial
                        )VALUES ('{}','{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}','{}', 
                        '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')
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
        # print(item)
        # 唯一id查询
        cursor.execute(self.query_sql.format(item['uid']))
        if cursor.fetchone():
            print(f"标题 {item['title']} ==== {item['uid']} 已存在！！！")
        else:
            cursor.execute(self.insert_sql.format(
                # item['id'],
                item['uid'],
                item['uuid'],
                item['title'],
                item['link'],
                item['intro'],
                item['abs'],
                escape_string(item['content']),
                # item['content'],
                item['publish_time'],
                item['purchaser'],
                item['proxy'],
                item['create_time'],
                item['update_time'],
                item['deleted'],
                item['province'],
                item['base'],
                item['type'],
                item['items'],
                item['data_source'],
                item['end_time'],
                item['status'],
                item['serial']
            ))
            print(f"新增公告==== {item['uid']} ======{item['title']}")