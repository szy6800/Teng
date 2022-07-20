# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
from twisted.enterprise import adbapi
from pymysql.converters import escape_string


class GansuxinwenPipeline(object):
    def __init__(self, pool):
        self.dbpool = pool
        # 插入语句
        self.insert_sql = """
            INSERT INTO xinwen2021(
                            uid, link, title, province, publish_time, create_time, author,
                            content, data_source, status, base
                        )VALUES ('{}','{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')
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
        cursor.execute(self.insert_sql.format(
            item['uid'],
            item['link'],
            item['title'],
            item['province'],
            item['publish_time'],
            item['create_time'],
            item['author'],
            escape_string(item['content']),
            item['data_source'],
            item['status'],
            item['base']
        ))
        print(f"新增公告==== {item['uid']} ======{item['title']}")