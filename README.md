## 阳光在线学堂

主要技术    Django，mysql，redis，vue，

第三方   CC视频，支付宝与微信支付接口

### 数据库表设计

```python
# 课程分类表
name = models.CharField(max_length=64, unique=True)


#课程表
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
me, self.get_course_type_display())


#课程详情页内容
course = models.OneToOneField("Course", on_delete=models.CASCADE)
hours = models.IntegerField("课时")
course_slogan = models.CharField(max_length=125, blank=True, null=True)
# 视频简介地址
# video_brief_link = models.CharField(max_length=255, blank=True, null=True)
# why_study = models.TextField(verbose_name="为什么学习这门课程")
# what_to_study_brief = models.TextField(verbose_name="我将学到哪些内容")
# career_improvement = models.TextField(verbose_name="此项目如何有助于我的职业生涯")
# prerequisite = models.TextField(verbose_name="课程先修要求", max_length=1024)
# 推荐课程
recommend_courses = models.ManyToManyField("Course", related_name="recommend_by", blank=True)
# 课程讲师
teachers = models.ManyToManyField("Teacher", verbose_name="课程讲师")



#讲师、导师表
name = models.CharField(max_length=32)
role_choices = ((0, '讲师'), (1, '导师'))
role = models.SmallIntegerField(choices=role_choices, default=0)
title = models.CharField(max_length=64, verbose_name="职位、职称")
# signature = models.CharField(max_length=255, help_text="导师签名", blank=True, null=True)
# 老师图片地址
image = models.CharField(max_length=128)
# 老师简介
brief = models.TextField(max_length=1024)



#价格与有课程效期表
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



#课程章节表
course = models.ForeignKey("Course", related_name='coursechapters', on_delete=models.CASCADE)
chapter = models.SmallIntegerField(verbose_name="第几章", default=1)
name = models.CharField(max_length=128)
summary = models.TextField(verbose_name="章节介绍", blank=True, null=True)
# is_create = models.BooleanField(verbose_name="是否创建题库进度", default=True)
pub_date = models.DateField(verbose_name="发布日期", auto_now_add=True)



# 用户相关表
#用户信息表
username = models.CharField("用户名", max_length=64, unique=True)
password = models.CharField('password', max_length=128)
# 阳光币
sunbi = models.IntegerField(default=100)
#token表
key = models.CharField(max_length=40)
user = models.OneToOneField(
	UserInfo, related_name='auth_token',
        on_delete=models.CASCADE, verbose_name="关联用户"
    )
# auto_now_add更新的时候,会更改时间
created = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)


# 优惠券相关表
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



#优惠券发放、消费纪录表
coupon = models.ForeignKey("Coupon", on_delete=models.CASCADE)
number = models.CharField(max_length=64)
# 跟用户什么关系?跟user是一对多的关系
user = models.ForeignKey("UserInfo", verbose_name="拥有者", on_delete=models.CASCADE)
status_choices = ((0, '未使用'), (1, '已使用'), (2, '已过期'))
status = models.SmallIntegerField(choices=status_choices, default=0)
get_time = models.DateTimeField(verbose_name="领取时间", help_text="用户领取时间")
used_time = models.DateTimeField(blank=True, null=True, verbose_name="使用时间")
```

### 课程支付相关

#### 购物车

	-往后台传输数据（价格策略id，课程id）
	-为什么要放到redis
	-存储数据方式：（key值为：shopping_card_userid）
	-校验规则：
			-校验课程是否存在
			-校验价格策略是否合法
			-把价格策略拼成一个字典，直接用id in 字典，判断价格策略是否合法
			-取出原来购物车的商品，更新，或者新增
				-传过来的id 在购物车字典中，只要修改默认价格策略即可
				-传过来的id不在购物车字典中，直接新增
			-存到redis
	-购物车逻辑： 
		-（1）添加购物车  ----post：{"course_id":"1","policy_id":"1"}
			-1 校验课程是否存在
			-2 获取所有价格策略
			-3 从redis中取出当前登录用户的购物车
			-4 循环价格策略组装成以下形式
			-5 校验价格策略是否是该课程的价格策略（判断传入的policy_id是否在上面的字典中）
			-6 价格策略合法，构造出购物车字典（如果购物车中有该课程，修改的是默认策略）
			-7 转成json，存入redis  name值为：'shopping_%s' % (request.user.id,)	
		-（2）修改购物车中某个课程价格策略
			-1 从redis中取出购物车
			-2 判断价格策略是否合法（也就是是否在当前课程的policy字典中）
			-3 在的话，直接修改default_policy为传入的policy_id
			-4 把数据写回redis	
		-（3）删除购物车中课程
			-1 从redis中取出购物车
			-2 从购物车中pop掉当前传入的course_id
			-3 把数据写会redis
		-（4）获取购物车---get
			-1 从redis中取出购物车
			-2 把购物车放到res.data 中返回

#### 结算中心	

```python

结算中心：
	-请求格式
	
	-存储格式（结算中心和全局优惠券格式）：
-全局优惠券格式

-结算中心逻辑分析：
	-（1）添加到结算中心
		-1 定义结算中心的字典，定义全局优惠券的字典
		-2 拿到购物车，循环取出传入的课程id，判断是否在购物车中，不在直接抛异常
		-3 构造单个课程详情的字典，把购物车中的当前课程，update到该字典中
		-4 将该课程详情，加入到结算中心（现在里面没有优惠券相关信息）（为了效率，不在for循环中查询数据库，查出优惠券）
		-5 一次性查出当前用户的所有优惠券信息（用户为当前用户，状态为未使用，优惠券起始时间小于当前时间，优惠券结束时间大于当前时间）
		-6 循环所有优惠券
		-7 构造出单个优惠券的空字典，拿到优惠券类型（1立减 2 满减 3折扣），拿到优惠券id，拿到该优惠券绑定的课程id（有可能为空）
		-8 构造单个优惠券字典，将数据填充进去
		-9 判断是全站优惠券还是课程优惠券
		-10 讲结算中心字典和全局优惠券字典，放入redis中
		-11 返回成功	
	-（2）修改结算中心某个课程的优惠券信息
		-1 从reids中取出结算中心数据
		-2 先校验coupon_id是否合法，也就是是否在结算中心的优惠券信息中
		-3 合法，直接修改，返回正确信息
	-（3）获取结算中心数据----get
		-1 从redis中取出本人的结算中心数据 
		-2 从redis中取出本人的全局优惠券数据 
		-3 构造数据返回前台
-去支付：
	-前端传递数据格式：
-去支付逻辑：
	-从支付中心拿出字典,全局优惠券字典取出来
	-循环结算中心字典，得到课程和课程id
	-取出默认价格策略，取出默认价格，取出默认优惠券id	
	-判断如果默认优惠券不为0，表示使用了优惠券：取出默认优惠券的字典，调用计算价格函数得到价格，把价格放到价格列表中（后面直接用sum函数计算总价格）
	-取出全局默认优惠券id，根据默认优惠券id取出全局优惠券字典，调用计算价格函数得到实际支付价格
	-判断阳光币数大于传入的阳光币数，用实际价格减去阳光币数，如果得到结果小于0，直接等于0，判断最终价格和传如的价格是否相等，不相等抛异常
	-如果实际支付价格大于0，生成支付宝url地址，返回给前端，让前端跳转
-计算价格方法：
	#传入价格和优惠券字典
		#设置总价格为price
		#取出优惠券类型
		#优惠券类型是0，立减
		##优惠券类型是1，满减，必须大于最低消费金额
		##优惠券类型是2，直接打折
```


​			