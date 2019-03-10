
# 自定义的异常类
class CommonException(Exception):
    def __init__(self,status,msg):
        self.status=status
        self.msg=msg