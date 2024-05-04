# _*_ coding:utf-8 _*_
from __future__ import unicode_literals
from datetime import datetime
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model

#机构类
class Organization(models.Model):
    name = models.CharField(max_length=50,verbose_name=u'机构名称')
    desc = models.TextField(verbose_name=u'机构描述')
    category = models.CharField(verbose_name='机构类别', default='高校',max_length=20,
                                choices=(('business','商业'),('private','私人'),('university','高校')))
    image = models.ImageField(upload_to= 'users/images/organization/', verbose_name=u'logo',blank=True)
    address = models.CharField(max_length=150,verbose_name=u'机构地址')
    students = models.IntegerField(default=0, verbose_name=u'学生人数')
    course_nums = models.IntegerField(default=0, verbose_name=u'课程数')
    add_time = models.DateTimeField(default=datetime.now)

    class Meta:
        verbose_name = u'学校机构'
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.name

#继承原有auth中user并且添加自定义user数据表
class UserProfile(AbstractUser):
    nick_name = models.CharField(max_length=50, verbose_name=u"昵称")
    birthday = models.DateField(verbose_name=u"生日", null=True, blank=True)
    gender = models.CharField(max_length=6, verbose_name=u"性别", choices=(("male",u"男"),("female","女")),
                              default="female")
    address = models.CharField(max_length=100, default=u"")
    mobile = models.CharField(max_length=11, null=True, blank=True)
    image = models.ImageField(upload_to=u"users/image/userprofile/",verbose_name=u"头像",blank=True,
                              default=u"users/image/userprofile/default.png", max_length=200)
    category = models.CharField(max_length=8, choices=(("student",u"学生"),("teacher","老师")),
                                default="student")
    org = models.ForeignKey(Organization,on_delete = models.CASCADE,
                            db_constraint=False, null=True, blank=True,related_name=u'所属机构')
    add_time = models.DateTimeField(default=datetime.now)
    self_introduction=models.TextField(default='', verbose_name='自我介绍', null=True, blank=True)

    class Meta:
        verbose_name = "个人用户"
        verbose_name_plural = verbose_name
    def save(self, *args, **kwargs):
        if not self.nick_name :
            self.nick_name = self.username
        super().save(*args, **kwargs)
    def __str__(self):
        return self.username #这里不能改，因为很过滤判断条件用到了 username=self.request.user,而不是写成 username=self.request.user.username


# class EmailVerifyRecord(models.Model):
#     code = models.CharField(max_length=20, verbose_name=u'验证码')
#     email = models.EmailField(max_length=50, verbose_name=u'邮箱')
#     send_type = models.CharField(verbose_name=u'验证码类型', choices=(('register',u'注册'),('forget',u'找回密码'),('update_email',u'修改邮箱')), max_length=30)
#     send_time = models.DateTimeField(verbose_name=u'发送时间',default=datetime.now)
#
#     class Meta:
#         verbose_name = u'邮箱验证码'
#         verbose_name_plural = verbose_name
#     def __unicode__(self):
#         return '{0}({1})'.format(self.code, self.email)


#
class VerifyCode(models.Model):
    """
    短信验证码
    """
    code = models.CharField(max_length=10, verbose_name="验证码")
    mobile = models.CharField(max_length=11, verbose_name="电话")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "短信验证码"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.code






