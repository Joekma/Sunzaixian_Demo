from django.shortcuts import render, HttpResponse
from rest_framework.views import APIView

from rest_framework.response import Response
from api import models
from api import MySer
from api.utils import MyResponse
from django.core.exceptions import ObjectDoesNotExist
from django.core.cache import cache
import uuid
from django_redis import get_redis_connection

from rest_framework.request import Request
class Login(APIView):
    def post(self, request):
        response = MyResponse()
        # post 提交的数据,request.data中取
        name = request.data.get('name')
        # 密码是明文   md5加密
        pwd = request.data.get('pwd')
        user = models.UserInfo.objects.filter(username=name, password=pwd).first()
        if user:
            # 处理token
            # 生成token
            token = uuid.uuid4()
            import datetime

            models.Token.objects.update_or_create(user=user, defaults={'key': token,'created':datetime.datetime.now()})
            # 用redis处理
            # conn=get_redis_connection()
            # user_dic={'id':user.pk,'name':user.name}
            # conn.hmset(token,user_dic)
            # redis放置结束

            # 把user对象放入缓存,key值是随机字符串asdfasdfasd
            cache.set(token,user,60*60*24)

            response.msg = '登录成功'
            response.token = token
            response.name = name
        else:
            response.msg = '用户名或密码错误'
            response.status = 101
        return Response(response.get_data)
