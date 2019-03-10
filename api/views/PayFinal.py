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
import datetime


class PayFinal(APIView):
    conn = get_redis_connection()
    authentication_classes = [LoginAuth]

    def post(self, request):
        response = MyResponse()
        # 传入的参数 {"price":600",beli":100}
        price_in = request.data.get('price')
        beli = request.data.get('beli')
        try:
            # 1 从支付中心拿出字典,全局优惠券字典取出来
            payment_dic = json.loads(self.conn.get('payment_%s' % request.user.pk))
            global_coupon = json.loads(self.conn.get('global_coupon_%s' % request.user.pk))
            # 定义一个用于存储所有课程价格的列表
            price_list = []
            # 2 循环结算中心字典
            for course_id, course in payment_dic.items():
                # 取出默认价格策略，取出默认价格，取出默认优惠券id
                default_policy_id = course['default_policy']
                default_price = course['policy'][default_policy_id]['price']
                default_coupon_id = course['default_coupon']
                if default_coupon_id != 0:
                    # 如果不等于0,表示使用了优惠券
                    coupon_dic = course['coupon'][str(default_coupon_id)]
                    default_price = self.account(default_price, coupon_dic)
                # 注意要在if外面往里添加
                price_list.append(default_price)
            # 3 取出使用的全局优惠券id和字典
            default_coupon_id = global_coupon['default_coupon']
            final_price = sum(price_list)
            if default_coupon_id != 0:
                # 使用了优惠券
                global_coupon_dic = global_coupon['coupon'][str(default_coupon_id)]
                final_price = self.account(sum(price_list), global_coupon_dic)
            # 4 判断传入的贝利数是否合法
            if beli > request.user.beli:
                raise CommonException(104, '传入的贝利数有问题')

            final_price = final_price - beli / 10
            # 修改贝利数
            request.user.beli = request.user.beli - beli
            request.user.save()
            if final_price < 0:
                final_price = 0
            if final_price != price_in:
                raise CommonException(105, '您传入的价格不合法')
            if not final_price ==0:
                #构造阿里支付
                pass
                response.url='阿里支付的地址'

        except CommonException as e:
            response.msg = e.msg
            response.status = e.status
        except Exception as e:
            response.msg = str(e)
            # 项目上线,用下面这个
            # response.msg = '您的操作有误'
            response.status = 109
        return Response(response.get_data)

    def account(self, price, coupon_dic):
        total_price = price
        # 取出优惠券类型
        coupon_type = coupon_dic['coupon_type']
        if coupon_type == '0':
            total_price = price - coupon_dic['money_equivalent_value']
            if total_price < 0:
                total_price = 0
        elif coupon_type == '1':
            if not price > coupon_dic['minimum_consume']:
                raise CommonException(103, '您选的优惠券不符合最低消费金额')
            total_price = price - coupon_dic['money_equivalent_value']
        else:
            total_price = price * coupon_dic['off_percent'] / 100
        return total_price
