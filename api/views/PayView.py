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


class Pay(APIView):
    # 拿到redis的链接
    conn = get_redis_connection()
    authentication_classes = [LoginAuth]

    def post(self, request):
        response = MyResponse()
        # 传入的数据{"course_list":[{"course_id":"1","policy_id":"1"},{"course_id":"2","policy_id":"2"}]}
        course_list = request.data.get('course_list')
        try:
            # 1定义结算中心的字典，定义全局优惠券的字典
            payment_dic = {}
            global_coupon_dic = {
                'coupon': {},
                'default_coupon': 0
            }
            # 2 取出购物车的数据
            shopping_cart_bytes = self.conn.get('shopping_cart_%s' % request.user.pk)
            shopping_cart_dic = json.loads(shopping_cart_bytes) if shopping_cart_bytes else {}
            # 3 循环传入的course_list值
            for course_id_dic in course_list:
                course_in_id = course_id_dic['course_id']
                if course_in_id not in shopping_cart_dic:
                    # 传入的数据不合法,要结算的课程不在购物车中
                    raise CommonException(102, '要结算的课程不在购物车中')
                # 4 构造出单个课程详情字典
                course_detail = {
                    'coupon': {},
                    'default_coupon':0
                }
                course_detail.update(shopping_cart_dic[course_in_id])
                # 5 把该课程详情添加到结算中心字典中
                payment_dic[course_in_id] = course_detail
            # 6 查询出所有优惠券,包括全站优惠券和课程优惠券(当前用户,未使用,当前在有效期内)
            # 取出当前时间,有效优惠券时间:优惠券开始时间小于当前时间,优惠券结束时间,大于当前时间
            ctime = datetime.datetime.now()
            coupon_list = models.CouponRecord.objects.filter(user=request.user,
                                                             status=0,
                                                             coupon__valid_begin_date__lte=ctime,
                                                             coupon__valid_end_date__gte=ctime
                                                             )
            # 7 循环所有优惠券
            for coupon in coupon_list:
                # 取出该优惠券类型,转str
                coupon_type = str(coupon.coupon.coupon_type)
                # 构造出单个优惠券详情的字典
                coupon_detail = {
                    'coupon_display': coupon.coupon.get_coupon_type_display(),
                    'coupon_type': coupon_type
                }
                # 取出优惠券id,课程id
                coupon_id = str(coupon.pk)
                coupon_course_id = coupon.coupon.object_id
                # 8 根据优惠券类型,继续往单个优惠券字典中添加字段
                if coupon_type == '0':
                    coupon_detail['money_equivalent_value'] = coupon.coupon.money_equivalent_value
                elif coupon_type == '1':
                    coupon_detail['money_equivalent_value'] = coupon.coupon.money_equivalent_value
                    coupon_detail['minimum_consume'] = coupon.coupon.minimum_consume
                else:
                    coupon_detail['off_percent'] = coupon.coupon.off_percent
                # 9 判断是全站优惠券还是课程优惠券
                if not coupon_course_id:
                    # 全局优惠券
                    global_coupon_dic['coupon'][coupon_id] = coupon_detail
                else:
                    # 课程优惠券(大坑)
                    # coupon_course_id 是当前优惠券对应的课程id,但是该课程不一定在结算中心中
                    if str(coupon_course_id) not in payment_dic:
                        continue
                    payment_dic[str(coupon_course_id)]['coupon'][coupon_id] = coupon_detail
            # 10 把结算中心字典,和全局优惠券字典放到redis中
            self.conn.set('payment_%s' % request.user.pk, json.dumps(payment_dic))
            self.conn.set('global_coupon_%s' % request.user.pk, json.dumps(global_coupon_dic))
            response.msg = '加入结算中心成功'
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
        response = MyResponse()
        response.payment = json.loads(self.conn.get('payment_%s' % request.user.pk))
        response.global_coupon = json.loads(self.conn.get('global_coupon_%s' % request.user.pk))
        response.msg = '查询成功'
        response.beli=request.user.beli
        return Response(response.get_data)
