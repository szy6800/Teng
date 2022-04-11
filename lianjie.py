# -*- coding: utf-8 -*-

# @Time : 2022/4/10 15:37
# @Author : 石张毅
# @Site : 
# @File : lianjie.py
# @Software: PyCharm 

# import pymysql
#
#
# def connect_mysql():
#     connect = pymysql.Connect(
#         host='localhost',
#         port=3306,
#         user='root',
#         password='123456',
#         db='stu',
#         charset='utf8',
#     )
#     # 创建游标对象
#     cursor = connect.cursor()
#     # sql语句
#     select_sql = """SELECT * FROM t_baby WHERE nickname='{}'"""
#     # delete_sql = """drop table student"""
#     # cursor.execute(delete_sql)
#     # 插入语句
#     insert_sql = """
#         INSERT INTO t_baby(nickname,sex)VALUES ('{}','{}')
#     """
#     name = 'eqw1打算'
#     age = 52
#     # 执行sql 语句
#     cursor.execute(select_sql.format(name))
#     # print(cursor.fetchone())
#     # 如果存在这条数据 就提示跳过
#     if cursor.fetchone():
#         print('数据存在')
#     else:
#         #否则就插入
#         cursor.execute(insert_sql.format(name,age))
#         # 必须提交
#         cursor.connection.commit()
#         print('数据已插入')
#
#
# connect_mysql()


a = [
{'provice':'澳门','city':'澳门'},
{'provice':'安徽','city':'合肥'},
{'provice':'安徽','city':'蚌埠'},
{'provice':'安徽','city':'芜湖'},
{'provice':'安徽','city':'马鞍山'},
{'provice':'福建省','city':'福州'},
{'provice':'福建省','city':'厦门'},

]

