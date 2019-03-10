# import redis
#
# POOL=redis.ConnectionPool(host='127.0.0.1',port=6379)


class MyResponse():
    def __init__(self):
        self.status=100
        self.msg=None
    @property
    def get_data(self):
        return self.__dict__