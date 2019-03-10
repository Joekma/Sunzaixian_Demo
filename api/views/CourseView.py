from django.shortcuts import render, HttpResponse
from rest_framework.views import APIView

from rest_framework.response import Response
from api import models
from api import MySer
from api.utils import MyResponse
from django.core.exceptions import ObjectDoesNotExist


class Courses(APIView):
    def get(self, request):
        response = MyResponse()
        course_list = models.Course.objects.all()
        course_ser = MySer.CourseSer(instance=course_list, many=True)
        response.msg = '查询成功'
        response.data = course_ser.data

        return Response(response.get_data)


from api.MyAuth import LoginAuth


class Course(APIView):
    authentication_classes = [LoginAuth, ]

    def get(self, request, pk):
        response = MyResponse()
        # pk 是课程的id,查询的是课程详情表******
        try:
            course_detail = models.CourseDetail.objects.get(course_id=pk)
            coursedetailser = MySer.CourseDetailSer(instance=course_detail, many=False)
            response.data = coursedetailser.data
        except ObjectDoesNotExist as e:
            response.msg = '该课程不存在'
            response.status = 101
        except Exception as e:
            response.msg = str(e)
            response.status = 105

        return Response(response.get_data)
