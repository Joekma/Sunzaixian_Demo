from rest_framework import serializers

from api import models

class PricePolicySer(serializers.ModelSerializer):
    class Meta:
        model = models.PricePolicy
        fields = "__all__"

class CourseSer(serializers.ModelSerializer):
    class Meta:
        model = models.Course
        fields = "__all__"

    level = serializers.CharField(source='get_level_display')
    price_policy=serializers.SerializerMethodField()
    def get_price_policy(self,obj):
        price_list=obj.price_policy.all()
        price_ser=PricePolicySer(instance=price_list,many=True)

        # 作业,返回最低价格
        return price_ser.data


class CourseDetailSer(serializers.ModelSerializer):
    class Meta:
        model = models.CourseDetail
        fields = "__all__"
    name=serializers.CharField(source='course.name')
    level = serializers.CharField(source='course.get_level_display')
    brief=serializers.CharField(source='course.brief')
    price_policy = serializers.SerializerMethodField()

    def get_price_policy(self, obj):
        price_list = obj.course.price_policy.all()
        price_ser = PricePolicySer(instance=price_list, many=True)
        return price_ser.data