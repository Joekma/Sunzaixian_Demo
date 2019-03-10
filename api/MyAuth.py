from rest_framework.authentication import BaseAuthentication
from django.core.cache import cache
from api import models
from rest_framework.exceptions import AuthenticationFailed

from django_redis import get_redis_connection


class LoginAuth(BaseAuthentication):
    def authenticate(self, request):
        # 作业,从头中取出token并认证
        token = request.GET.get('token')

        # ############从redis中获取
        # conn=get_redis_connection()
        # user_dic=conn.hmget(token)
        # if user_dic:
        #     return user_dic,token
        # ############结束##############
        # 在缓存中这么存
        # asdfasdfasf:user对象
        user = cache.get(token)
        if user:
            return user, token
        # 如果从缓存中取不到,再去数据库中取
        token = models.Token.objects.filter(key=token).first()
        if token:
            # request.user=token.user
            return token.user, token
        else:
            raise AuthenticationFailed('您没有登录')
