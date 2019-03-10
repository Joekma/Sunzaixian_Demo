from django.contrib import admin

# Register your models here.
from api import models
admin.site.register(models.Course)
admin.site.register(models.CourseCategory)
admin.site.register(models.CourseChapter)
admin.site.register(models.CourseDetail)
admin.site.register(models.PricePolicy)
admin.site.register(models.Teacher)
admin.site.register(models.UserInfo)
admin.site.register(models.Token)
admin.site.register(models.Coupon)
admin.site.register(models.CouponRecord)