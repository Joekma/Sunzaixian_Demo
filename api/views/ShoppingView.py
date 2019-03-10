from django.shortcuts import render, HttpResponse
from rest_framework.views import APIView

from rest_framework.response import Response
from api import models
from api import MySer
from api.utils import MyResponse
from django.core.exceptions import ObjectDoesNotExist
from api.MyAuth import LoginAuth
from api.MyException import CommonException
from django_redis import get_redis_connection
import json


class Shopping(APIView):
    # 拿到redis的链接
    conn = get_redis_connection()
    authentication_classes = [LoginAuth]

    def post(self, request):
        response = MyResponse()
        # 传入的数据{"course_id":"1","policy_id":"1"}
        course_id = request.data.get('course_id')
        policy_id = request.data.get('policy_id')
        try:
            # 1  校验课程是否存在
            course = models.Course.objects.get(pk=course_id)
            # 2 取出所有价格策略
            policy_price_list = course.price_policy.all()
            # 3 取出redis中的购物车数据
            # 购物车数据的key值  shopping_cart_用户id
            # 因为有了认证组件,所以request.user就是当前登录用户
            shopping_cart_bytes = self.conn.get('shopping_cart_%s' % request.user.pk)
            shopping_cart_dic = json.loads(shopping_cart_bytes) if shopping_cart_bytes else {}
            # 跟上面一样
            # if shopping_cart_bytes:
            #     shopping_cart_dic=json.loads(shopping_cart_bytes)
            # else:
            #     shopping_cart_dic={}
            # 4 用于存放所有价格策略的字典,循环所有的价格策略
            policy = {}
            for policy_price in policy_price_list:
                policy[str(policy_price.pk)] = {
                    'period': policy_price.valid_period,
                    # 取出价格周期的文字
                    'period_display': policy_price.get_valid_period_display(),
                    'price': policy_price.price
                }
            if policy_id not in policy:
                # 5 传入的价格策略不合法,不在该课程的所有价格策略中
                raise CommonException(102, '价格策略不合法,你是爬虫')
            # 6 判断当前传入的课程id是否在购物车中,在则更新
            if course_id in shopping_cart_dic:
                shopping_cart_dic[course_id]['default_policy'] = policy_id
                response.msg = '更新购物车成功'
            else:
                shopping_cart_dic[course_id] = {
                    'title': course.name,
                    'img': course.course_img,
                    # 默认价格策略,是传入的价格策略id
                    'default_policy': policy_id,
                    'policy': policy
                }
                response.msg = '添加购物车成功'
            # 7 把字典转成字符串,存入redis
            self.conn.set('shopping_cart_%s' % request.user.pk, json.dumps(shopping_cart_dic))

        except ObjectDoesNotExist as e:
            response.msg = '该课程不存在,你可能是爬虫'
            response.status = 101
        except CommonException as e:
            response.msg = e.msg
            response.status = e.status
        except Exception as e:
            response.msg = str(e)
            # 项目上线,用下面这个
            # response.msg = '您的操作有误'
            response.status = 109
        return Response(response.get_data)

    def get(self, request):
        # 获取购物车接口
        response = MyResponse()
        shopping_cart_bytes = self.conn.get('shopping_cart_%s' % request.user.pk)
        shopping_cart_dic = json.loads(shopping_cart_bytes) if shopping_cart_bytes else {}
        response.msg = '查询购物车成功'
        response.data = shopping_cart_dic
        return Response(response.get_data)

    def put(self, request):
        response = MyResponse()
        # 传入的数据{"course_id":"1","policy_id":"2"}
        course_id = request.data.get('course_id')
        policy_id = request.data.get('policy_id')
        shopping_cart_bytes = self.conn.get('shopping_cart_%s' % request.user.pk)
        shopping_cart_dic = json.loads(shopping_cart_bytes) if shopping_cart_bytes else {}
        try:
            # 判断课程是否在购物车字典中
            if course_id not in shopping_cart_dic:
                # 说明可定不是正常
                raise CommonException(102, '要修改的课程不存在')
            # 判断价格策略是否合法,是否在当前课程的所有价格策略中
            if policy_id not in shopping_cart_dic[course_id]['policy']:
                raise CommonException(103, '要修改的价格策略不合法')
            # 修改默认价格策略
            shopping_cart_dic[course_id]['default_policy'] = policy_id
            # 存入reids
            self.conn.set('shopping_cart_%s' % request.user.pk, json.dumps(shopping_cart_dic))
            response.msg = '更新成功'
        except CommonException as e:
            response.status = e.status
            response.msg = e.msg
        except Exception as e:
            response.msg = str(e)
            # 项目上线,用下面这个
            # response.msg = '您的操作有误'
            response.status = 109
        return Response(response.get_data)

    def delete(self, request):
        response = MyResponse()
        # 传列表形式
        # "course_id_list":['1','2','3',100]
        course_id_list = request.data.get('course_id_list')
        # 获取购物车地址
        shopping_cart_bytes = self.conn.get('shopping_cart_%s' % request.user.pk)
        shopping_cart_dic = json.loads(shopping_cart_bytes) if shopping_cart_bytes else {}
        try:
            for course_id in course_id_list:
                if course_id not in shopping_cart_dic:
                    raise CommonException(102, '您传入的课程不合法')
                shopping_cart_dic.pop(course_id)
            self.conn.set('shopping_cart_%s' % request.user.pk, json.dumps(shopping_cart_dic))
            response.msg = '删除成功'
        except CommonException as e:
            response.status = e.status
            response.msg = e.msg
        except Exception as e:
            response.msg = str(e)
            # 项目上线,用下面这个
            # response.msg = '您的操作有误'
            response.status = 109
        return Response(response.get_data)



