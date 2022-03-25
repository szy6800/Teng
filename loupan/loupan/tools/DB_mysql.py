import pymysql

from loupan.settings import *


conn = pymysql.connect(
    host=MYSQL_HOST,
    port=MYSQL_PORT,
    user=MYSQL_USER,
    password=MYSQL_PASSWD,
    database=MYSQL_DB,
    charset='utf8',
    cursorclass=pymysql.cursors.SSCursor
)

cursor = conn.cursor()
