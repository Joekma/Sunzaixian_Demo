import redis

# # 拿到一个redis链接,普通链接
conn = redis.Redis(host='127.0.0.1', port=6379)

# 连接池
# # 正常情况pool是单例的
# pool = redis.ConnectionPool(host='127.0.0.1', port=6379)
# # 只要执行这句,就会从池子中拿一个连接
# conn = redis.Redis(connection_pool=pool)

# 字符串操作
# conn.set('yyy', 'egon', nx=True)
# conn.set('ttt', 'egon', xx=True)
# import datetime
# v=datetime.timedelta(weeks=2)
# ctime=datetime.datetime.now()
# ctime+v
# conn.setex('ttt', 5,'xxx')

# conn.mset({"k1": 'v1', "k2": 'v12', "k3": 'v3'})
# value=conn.mget('name','k1','k2')
# value=conn.mget(['name','k1','k2'])
# print(value)
# print(conn.getset('name','xxxxxx'))
# conn.setrange('name', 1, 'eerrrrrrrrrrrrrrrr')

# print(conn.strlen('name'))
# conn.set('age',"19")
# 文章阅读数
# conn.incr('age',-4)
# conn.append('name','0000000')


# 字典操作

# conn.hset('person','age','18')
# conn.hset('person','name','lqz')
# conn.hset('person','height','180')
# conn.hmset('person2',{'age':'19','name':'egon','xx':'xx'})
# print(conn.hget('person','name'))
# print(conn.hmget('person','age','name','height'))
# print(conn.hmget('person',['age','name','height']))
# 以后用这个要慎用
# print(conn.hgetall('person'))
# print(conn.hlen('person'))
# print(conn.hkeys('person'))

# print(conn.hexists('person','nameee'))
# conn.hdel('person2','name','age')

# conn.hincrby('person','age')
# for i in range(1000000):
#     conn.hmset('person2',{'eeeeee%s'%i:i})
# 如果数据量不大,自动全取出来
# cour, data = conn.hscan('person2', cursor=0, match=None, count=3000)
# cour2, data2 = conn.hscan('person2', cursor=cour, match=None, count=3000)
#
# print(cour)
# print(len(data))
#
# print('-------')
# print(cour2)
# print(len(data2))

# cour2 = 0
# count = 1
# while True:
#     cour2, data2 = conn.hscan('person2', cursor=cour2, match=None, count=3000)
#     count += len(data2)
#     if cour2 == 0:
#         break
#
# print(count)
# 不用getall的方式取,用这种方式取,也能把所有数据取出来,但是不会吧内存撑爆
# data=conn.hscan_iter('person2', match=None, count=100)
# # 内部有915371条数据
# # 先去取100条
# # 做成了生成器
# # 取值的时候,100以内,没有再去查,用的是生成器
# # 当超过一百,再去取100条.做成了生成器
# for i in data:
#     print(i)

# 列表操作

# conn.lpush('list','2')
# conn.rpush('list','3')
# conn.lpushx('list2','3')
# print(conn.llen('list'))

# conn.linsert('list', 'after', "3", '444444')
# conn.linsert('list', 'before', "3", '5555555')
# 从0开始
# conn.lset('list',4,'66666666')
# conn.lrem('list',0,"3")
# print(conn.lpop('list'))
# print(conn.rpop('list'))
# 按索引取值,支持负索引
# print(conn.lindex('list',-2))

# 简单的分布式爬虫
# print(conn.blpop('list'))
# 取出列表的所有值

# conn.lpush('list',*[1,2,3,4,45,5,6,7,7,8,43,5,6,768,89,9,65,4,23,54,6757,8,68])
# print(conn.lrange('list',0,-1))
# 自定义列表的增量迭代
# def scan_list(name,count=2):
#     index=0
#     while True:
#         data_list=conn.lrange(name,index,count+index-1)
#         if not data_list:
#             return
#         index+=count
#         for item in data_list:
#             yield item
# # print(conn.lrange('test',0,100))
# for item in scan_list('list',5):
#     print('---')
#     print(item)

# 其它操作

# 事务(不支持事务,但是通过管道模拟)
conn=redis.Redis(host='127.0.0.1', port=6379)
# 拿到一个管道,transaction=True表示管道内部都是原子性
pi=conn.pipeline(transaction=True)
# 说明是批量命令
pi.multi()


pi.set('xx','xxx')
pi.set('yy','yyy')

pi.execute()

# 其它操作
# conn.delete('name1')
# 用的比较多
# print(conn.keys('k*'))

# print(conn.type('person'))
# django中使用redis
