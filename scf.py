# -*- coding: utf-8 -*-

# @Time : 2022/3/10 18:16
# @Author : 石张毅
# @Site : 
# @File : scf.py
# @Software: PyCharm

import pymysql


def connect_mysql():
    connect = pymysql.Connect(
        host='localhost',
        port=3306,
        user='root',
        password='123456',
        db='stu',
        charset='utf8',
    )
    # 创建游标对象
    cursor = connect.cursor()
    # sql语句
    select_sql = """SELECT * FROM student WHERE name='{}'"""
    # delete_sql = """drop table student"""
    # cursor.execute(delete_sql)
    # 插入语句
    insert_sql = """
        INSERT INTO student(name,age)VALUES ('{}','{}')
    """
    name = '石张毅'
    age = 52
    # 执行sql 语句
    cursor.execute(select_sql.format(name))
    # print(cursor.fetchone())
    # 如果存在这条数据 就提示跳过
    if cursor.fetchone():
        print('数据存在')
    else:
        #否则就插入
        cursor.execute(insert_sql.format(name,age))
        # 必须提交
        cursor.connection.commit()
        print('数据已插入')

connect_mysql()