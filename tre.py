import redis
from JSTT.settings import *

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
        redis_id = Redis_DB().r.hexists('wenzhangquchong', key=id)
        if redis_id == True:
            return True
        else:
            Redis_DB().r.hset('wenzhangquchong', id, id)
