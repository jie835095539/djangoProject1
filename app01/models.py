from django.db import models


class Admin(models.Model):
    username = models.CharField(verbose_name="管理员姓名", max_length=64)
    password = models.CharField(verbose_name="登录密码", max_length=128)
    account = models.CharField(verbose_name="管理员账号", max_length=64)

    def __str__(self):
        return self.username

# Create your models here.
"""部门表"""


class Department(models.Model):
    depart_name = models.CharField(verbose_name="部门名称", max_length=64)
    company = models.CharField(verbose_name="公司名称", max_length=128)

    def __str__(self):
        return self.depart_name


"""员工表"""


class UserInfo(models.Model):
    name = models.CharField(verbose_name="员工姓名", max_length=32)
    password = models.CharField(verbose_name="密码", max_length=64)
    age = models.IntegerField(verbose_name="年龄")
    mobile = models.CharField(verbose_name="手机号", max_length=128)
    account = models.DecimalField(verbose_name="账户", max_digits=10, decimal_places=2, default=0)
    create_time = models.DateTimeField(verbose_name="创建时间", null=True)
    # 员工中的部门名称，有约束的情况
    # -to,与哪一张表进行关联
    # -to_fields,与表中的那一列关联
    # on_delete=models.CASCADE，删除用户数据
    # depart = models.ForeignKey(to="Department",to_field="id",on_delete=models.CASCADE)
    depart = models.ForeignKey(to="Department", to_field="id", null=True, blank=True,
                               on_delete=models.SET_NULL)  # 将部门信息设置为空
    gender_choice = ((1, "男"), (2, "女"))
    gender = models.SmallIntegerField(verbose_name="性别", choices=gender_choice, null=True)

    def __str__(self):
        return self.name



class MobileAccount(models.Model):
    """靓号管理表"""
    mobile = models.CharField(verbose_name="手机号", max_length=11)
    price = models.DecimalField(verbose_name="价格", max_digits=10, decimal_places=2, default=0)
    level_choice = ((1, "一星"), (2, "二星"), (3, "三星"), (4, "四星"), (5, "五星"))
    level = models.SmallIntegerField(verbose_name="级别", choices=level_choice, null=True)
    status_choice = ((0, "未占用"), (1, "已占用"))
    status = models.SmallIntegerField(verbose_name="状态", choices=status_choice, null=True)
    isdelect_choice = ((0, "有效"), (1, "无效"))
    isdelect = models.SmallIntegerField(verbose_name="是否有效", choices=isdelect_choice, default=0)


class Task(models.Model):
    """任务列表"""
    level_choice = (
        (1, "一般"),
        (2, "中等"),
        (3, "紧急")
    )
    level = models.SmallIntegerField(verbose_name="任务等级", choices=level_choice, default=1)
    title = models.CharField(verbose_name="任务标题", max_length=64)
    remark = models.TextField(verbose_name="详细描述", max_length=256)
    do_user = models.ForeignKey(to="UserInfo", to_field="id", null=True, blank=True,
                           on_delete=models.SET_NULL,verbose_name="执行人")
    create_time = models.DateTimeField(verbose_name="创建时间", null=True)
class Order(models.Model):
    """订单管理表"""
    oid = models.CharField(verbose_name="订单号",max_length=64)
    title = models.CharField(verbose_name="货物名称",max_length=128)
    price = models.CharField(verbose_name="价格",max_length=32)
    status_choice = (
        (1,"待支付"),
        (2,"已支付")
    )
    status = models.SmallIntegerField(verbose_name="支付状态",choices=status_choice,default=1)
    admin = models.ForeignKey(verbose_name="管理员",to="Admin",to_field="id",null=True, blank=True,on_delete=models.SET_NULL)