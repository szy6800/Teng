# -*- coding: utf-8 -*-

# @Time : 2022/3/4 14:50
# @Author : Szy
from redis import *
# from Bsdcomm.settings import *

REDIS_IP = '127.0.0.1'
REDIS_PORT = '6379'
REDIS_DB = 1
REDIS_PASSWD = ''

# pool = redis.ConnectionPool(host=REDIS_IP, port=REDIS_PORT, db=REDIS_DB, password=REDIS_PASSWD)  # , max_connections=10
# r = redis.Redis(connection_pool=pool)


class Redis_DB():

    __red = None
    __init = True

    def __new__(cls, *args, **kwargs):
        if cls.__red is None:
            cls.__red = object.__new__(cls)
        return cls.__red

    def __init__(self):
        if Redis_DB.__init:
            pool = ConnectionPool(host=REDIS_IP,
                                        port=REDIS_PORT,
                                        db=REDIS_DB,
                                        password=REDIS_PASSWD,
                                        max_connections=1000
                                        )
            self.r = Redis(connection_pool=pool)
            Redis_DB.__init = False


redis = Redis_DB().r
id = 'md5'
if redis.hsetnx('polic1', id, '') == 0:
    print(id, '\033[1;31m<<<------此项目已经采集过了------>>>\033[0m')
else:
    print('项目已存在')