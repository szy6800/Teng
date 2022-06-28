# -*- coding: utf-8 -*-

# @Time : 2022/3/4 14:50
# @Author : Szy
from redis import *
# from Bsdcomm.settings import *
import redis
# REDIS_IP = '127.0.0.1'
# REDIS_PORT = '6379'
# REDIS_DB = 1
# REDIS_PASSWD = ''

REDIS_IP = '123.56.87.41'
REDIS_PORT = 6379
REDIS_DB = 0
REDIS_PASSWD = '$SMe9ndaZQw$4bJ2'

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
            pool = redis.ConnectionPool(host=REDIS_IP,
                                        port=REDIS_PORT,
                                        db=REDIS_DB,
                                        password=REDIS_PASSWD,
                                        max_connections=1000
                                        )
            self.r = redis.Redis(connection_pool=pool)
            Redis_DB.__init = False

    """文章去重"""
    def Redis_pd(self, id):
        redis_id = Redis_DB().r.hexists('bulongquchong', key=id)
        if redis_id == True:
            return True
        else:
            Redis_DB().r.hset('bulongquchong', id, '')
