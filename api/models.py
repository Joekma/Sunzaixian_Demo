from django.db import models

# Create your models here.
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation


# 课程分类表
class CourseCategory(models.Model):
    name = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return "%s" % self.name

    class Meta:
        verbose_name = "课程分类"
        verbose_name_plural = "课程分类"


class Course(models.Model):
    """
    免费课程
    """
    name = models.CharField(max_length=128, unique=True, verbose_name="课程名")
    # 课程图片的地址
    course_img = models.CharField(max_length=255)
    course_type_choices = ((0, '付费'), (1, 'VIP专享'), (2, '学位课程'))
    course_type = models.SmallIntegerField(choices=course_type_choices)
    # 课程简介
    brief = models.TextField(verbose_name="课程概述", max_length=2048)
    # 课程登记
    level_choices = ((0, '初级'), (1, '中级'), (2, '高级'))
    level = models.SmallIntegerField(choices=level_choices, default=1)

    pub_date = models.DateField(verbose_name="发布日期", blank=True, null=True)
    # 建议学习多少天
    period = models.PositiveIntegerField(verbose_name="建议学习周期(days)", default=7)
    # 课程顺序;  help_text用在admin中的提示信息
    order = models.IntegerField("课程顺序", help_text="从上一个课程数字往后排")
    # 课程课件的存放位置
    attachment_path = models.CharField(max_length=128, verbose_name="课件路径", blank=True, null=True)

    status_choices = ((0, '上线'), (1, '下线'), (2, '预上线'))
    status = models.SmallIntegerField(choices=status_choices, default=0)
    # 课程分类,表示该课程是python,linux或者go
    course_category = models.ForeignKey("CourseCategory", on_delete=models.CASCADE, null=True, blank=True)

    # 跟订单表做关联
    # order_details = GenericRelation("OrderDetail", related_query_name="course")
    # 跟优惠券表做关联
    # coupon = GenericRelation("Coupon")
    # 跟价格策略表做关联
    price_policy = GenericRelation("PricePolicy")  # 用于GenericForeignKey反向查询，不会生成表字段，切勿删除，如有疑问请联系老村长

    def __str__(self):
        return "%s(%s)" % (self.name, self.get_course_type_display())


class CourseDetail(models.Model):
    """课程详情页内容"""

    course = models.OneToOneField("Course", on_delete=models.CASCADE)
    hours = models.IntegerField("课时")
    course_slogan = models.CharField(max_length=125, blank=True, null=True)
    # 视频简介地址
    # video_brief_link = models.CharField(max_length=255, blank=True, null=True)
    #
    # why_study = models.TextField(verbose_name="为什么学习这门课程")
    # what_to_study_brief = models.TextField(verbose_name="我将学到哪些内容")
    # career_improvement = models.TextField(verbose_name="此项目如何有助于我的职业生涯")
    # prerequisite = models.TextField(verbose_name="课程先修要求", max_length=1024)

    # 推荐课程
    recommend_courses = models.ManyToManyField("Course", related_name="recommend_by", blank=True)
    # 课程讲师
    teachers = models.ManyToManyField("Teacher", verbose_name="课程讲师")

    def __str__(self):
        return "%s" % self.course


class Teacher(models.Model):
    """讲师、导师表"""

    name = models.CharField(max_length=32)
    role_choices = ((0, '讲师'), (1, '导师'))
    role = models.SmallIntegerField(choices=role_choices, default=0)
    title = models.CharField(max_length=64, verbose_name="职位、职称")

    # signature = models.CharField(max_length=255, help_text="导师签名", blank=True, null=True)
    # 老师图片地址
    image = models.CharField(max_length=128)
    # 老师简介
    brief = models.TextField(max_length=1024)

    def __str__(self):
        return self.name


class PricePolicy(models.Model):
    """价格与有课程效期表"""
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)  # 关联course or degree_course
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    # course = models.ForeignKey("Course")
    valid_period_choices = ((1, '1天'), (3, '3天'),
                            (7, '1周'), (14, '2周'),
                            (30, '1个月'),
                            (60, '2个月'),
                            (90, '3个月'),
                            (120, '4个月'),
                            (180, '6个月'), (210, '12个月'),
                            (540, '18个月'), (720, '24个月'),
                            (722, '24个月'), (723, '24个月'),
                            )
    valid_period = models.SmallIntegerField(choices=valid_period_choices)
    price = models.FloatField()

    class Meta:
        unique_together = ("content_type", 'object_id', "valid_period")

    def __str__(self):
        return "%s(%s)%s" % (self.content_object, self.get_valid_period_display(), self.price)


class CourseChapter(models.Model):
    """课程章节"""
    course = models.ForeignKey("Course", related_name='coursechapters', on_delete=models.CASCADE)
    chapter = models.SmallIntegerField(verbose_name="第几章", default=1)
    name = models.CharField(max_length=128)
    summary = models.TextField(verbose_name="章节介绍", blank=True, null=True)
    # is_create = models.BooleanField(verbose_name="是否创建题库进度", default=True)
    pub_date = models.DateField(verbose_name="发布日期", auto_now_add=True)

    class Meta:
        unique_together = ("course", 'chapter')

    def __str__(self):
        return "%s:(第%s章)%s" % (self.course, self.chapter, self.name)



# 用户相关表
from django.utils.safestring import mark_safe
from django.contrib.auth.models import AbstractUser


class UserInfo(models.Model):
    username = models.CharField("用户名", max_length=64, unique=True)
    password = models.CharField('password', max_length=128)
    # 贝利
    beli = models.IntegerField(default=100)

    class Meta:
        verbose_name = '账户信息'
        verbose_name_plural = "账户信息"

    def __str__(self):
        return "%s" % (self.username)


class Token(models.Model):
    key = models.CharField(max_length=40)
    user = models.OneToOneField(
        UserInfo, related_name='auth_token',
        on_delete=models.CASCADE, verbose_name="关联用户"
    )

    # auto_now_add更新的时候,会更改时间
    created = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)

    def __str__(self):
        return self.key


# 优惠券相关
class Coupon(models.Model):
    """优惠券生成规则"""
    name = models.CharField(max_length=64, verbose_name="活动名称")
    brief = models.TextField(blank=True, null=True, verbose_name="优惠券介绍")
    coupon_type_choices = ((0, '立减券'), (1, '满减券'), (2, '折扣券'))
    coupon_type = models.SmallIntegerField(choices=coupon_type_choices, default=0, verbose_name="券类型")

    money_equivalent_value = models.IntegerField(verbose_name="等值货币", blank=True, null=True)
    off_percent = models.PositiveSmallIntegerField("折扣百分比", help_text="只针对折扣券，例7.9折，写79", blank=True, null=True)
    minimum_consume = models.PositiveIntegerField("最低消费", default=0, help_text="仅在满减券时填写此字段")

    # 这三个字段可以唯一关联到一个课程上
    # object_id如果为空,说明是全局优惠券,如果有值,就是课程又回去
    content_type = models.ForeignKey(ContentType, blank=True, null=True, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField("绑定课程", blank=True, null=True, help_text="可以把优惠券跟课程绑定")
    content_object = GenericForeignKey('content_type', 'object_id')

    quantity = models.PositiveIntegerField("数量(张)", default=1)
    open_date = models.DateField("优惠券领取开始时间")
    close_date = models.DateField("优惠券领取结束时间")
    valid_begin_date = models.DateField(verbose_name="有效期开始时间", blank=True, null=True)
    valid_end_date = models.DateField(verbose_name="有效结束时间", blank=True, null=True)

    coupon_valid_days = models.PositiveIntegerField(verbose_name="优惠券有效期（天）", blank=True, null=True,
                                                    help_text="自券被领时开始算起")
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "31. 优惠券生成规则"

    def __str__(self):
        return "%s(%s)" % (self.get_coupon_type_display(), self.name)


class CouponRecord(models.Model):
    """优惠券发放、消费纪录"""

    coupon = models.ForeignKey("Coupon", on_delete=models.CASCADE)
    number = models.CharField(max_length=64)
    # 跟用户什么关系?跟user是一对多的关系
    user = models.ForeignKey("UserInfo", verbose_name="拥有者", on_delete=models.CASCADE)
    status_choices = ((0, '未使用'), (1, '已使用'), (2, '已过期'))
    status = models.SmallIntegerField(choices=status_choices, default=0)
    get_time = models.DateTimeField(verbose_name="领取时间", help_text="用户领取时间")
    used_time = models.DateTimeField(blank=True, null=True, verbose_name="使用时间")

    class Meta:
        verbose_name_plural = "32. 优惠券发放、消费纪录"

    def __str__(self):
        return '%s-%s-%s' % (self.user, self.number, self.status)
