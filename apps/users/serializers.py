import os
from pathlib import Path

from courses.models import Course
from mooc1 import settings
from .models import UserProfile, Organization, VerifyCode
import re
from rest_framework import serializers
from django.contrib.auth import get_user_model
from datetime import datetime
import time
from datetime import timedelta
from rest_framework.validators import UniqueValidator

# from .models import VerifyCode

from mooc1.settings import REGEX_MOBILE


User = get_user_model()
class SmsSerializer(serializers.Serializer):
    mobile = serializers.CharField(max_length=11)
    def validate_mobile(self, mobile):
        """
        验证手机号码
        :param data:
        :return:
        """
        # 手机是否注册
        if User.objects.filter(mobile=mobile).count():
            raise serializers.ValidationError("用户已经存在")

        # 验证手机号码是否合法
        if not re.match(REGEX_MOBILE, mobile):
            raise serializers.ValidationError("手机号码非法")

        # 验证码发送频率
        one_mintes_ago = datetime.now() - timedelta(hours=0, minutes=1, seconds=0)
        if VerifyCode.objects.filter(add_time__gt=one_mintes_ago, mobile=mobile).count():
            raise serializers.ValidationError("距离上一次发送未超过60s")
        #验证通过，返回手机号
        return mobile

def img_proccess_save(image):
    # 防重名
    name = Path(image.name)#name.stem(文件名)、name.suffix(文件后缀)
    img_pure_name = name.stem + '_' + str(int(time.time())) # 文件名加时间戳
    img_extend_name = name.suffix # 提取后缀名
    img_name = img_pure_name + img_extend_name # 新的文件名
    # 新文件路径
    new_path_name = os.path.join('users/image/userprofile/', img_name)
    # 文件写入
    f = open(os.path.join(settings.MEDIA_ROOT, new_path_name), 'wb+')
    for chunk in image.chunks():  # 对图片切片
        f.write(chunk)  # 把切片写入
    f.close()
    return new_path_name
class UserDetailSerializer(serializers.ModelSerializer):
    """
    用户详情序列化类
    """
    username=serializers.CharField(read_only=True)
    # image_file = serializers.Field()
    image_file=serializers.ImageField(write_only=True,allow_null=True)#用于接收头像文件对象
    class Meta:
        model = User
        fields = ("id","nick_name","username", "gender", "birthday", "email", "mobile",'image','image_file')
    def update(self, instance, validated_data):
        image_file = validated_data.get('image_file', instance.image)
        if image_file:
            try:
                os.remove(os.path.join(settings.MEDIA_ROOT, str(instance.image)))  # 删除原头像
                print('文件删除成功')
            except:
                print('文件不存在')
            new_path_name=img_proccess_save(image_file)#写入新文件
            instance.image = new_path_name#更新路径

        instance.nick_name=validated_data.get('nick_name', instance.nick_name)
        instance.birthday = validated_data.get('birthday', instance.birthday)
        instance.gender = validated_data.get('gender', instance.gender)
        instance.mobile = validated_data.get('mobile', instance.mobile)
        instance.email = validated_data.get('email', instance.email)
        instance.save()

        return instance

class OrganizationSerializer(serializers.ModelSerializer):
    #category =CategorySerializer()
    courses = serializers.PrimaryKeyRelatedField(many=True,
                                                 queryset=Course.objects.all())
    class Meta :
        model = Organization
        fields = ['id','name','desc','category','image','courses']

class UserRegSerializer(serializers.ModelSerializer):
    '''
    用户注册序列化类
    '''
    #required=True代表必须有该字段
    code = serializers.CharField(required=True, write_only=True, max_length=4, min_length=4,label="验证码",
                                 error_messages={
                                     "blank": "请输入验证码1",
                                     "max_length": "验证码格式错误",
                                     "min_length": "验证码格式错误"
                                 },
                                 help_text="验证码")
    username = serializers.CharField(label="用户名", help_text="用户名", required=True, allow_blank=False,
                                     validators=[UniqueValidator(queryset=User.objects.all(), message="用户已经存在")])

    password = serializers.CharField(
        style={'input_type': 'password'},help_text="密码", label="密码", write_only=True,
    )
    mobile = serializers.CharField(max_length=11)

    def create(self, validated_data):
        user = super(UserRegSerializer, self).create(validated_data=validated_data)
        user.set_password(validated_data["password"])
        user.save()
        return user

    def validate_code(self, code):
        #
        verify_records = VerifyCode.objects.filter(mobile=self.initial_data["mobile"]).order_by("-add_time")
        if verify_records:
            last_record = verify_records[0]

            five_mintes_ago = datetime.now() - timedelta(hours=0, minutes=5, seconds=0)
            if five_mintes_ago > last_record.add_time:
                raise serializers.ValidationError("验证码过期")

            if last_record.code != code:
                raise serializers.ValidationError("验证码错误")

        else:
            raise serializers.ValidationError("验证码错误")

    def validate_mobile(self, mobile):
        # 手机是否注册
        if User.objects.filter(mobile=mobile).count():
            raise serializers.ValidationError("用户已经存在")
        # 验证手机号码是否合法
        if not re.match(REGEX_MOBILE, mobile):
            raise serializers.ValidationError("手机号码非法")
        #验证通过，返回手机号
        return mobile
    #validate作用于所有字段，因为我们想直接将用户名赋值给手机号，这也是我们在models中设计mobile可以为空的原因
    def validate(self, attrs):
        # attrs["mobile"] = attrs["username"]
        del attrs["code"] #因为user表中不需要存code，所以删除
        return attrs

    class Meta:
        model = User
        #这里一般是和前端对应，当然通过validate可以操作，这里写的字段我们直接访问链接时都会呈现
        fields = ("username", "code", "mobile", "password")

class PasswordUpdateSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(required=True, write_only=True)
    new_password=serializers.CharField(required=True,write_only=True)
    username = serializers.CharField(read_only=True)
    class Meta:
        model = User
        fields = ["id","username","old_password","new_password"]

    def update(self, instance, validated_data):
        ret= instance.check_password(validated_data['old_password'])
        if ret:#原密码正确
            instance.set_password(validated_data['new_password'])
            instance.save()
        else:
            raise serializers.ValidationError("原密码错误")
        return instance
class UserInfoListSerializer(serializers.ModelSerializer):
    '''用于公共展示教师或者学生信息'''
    org_name=serializers.ReadOnlyField(source='org.name')
    class Meta:
        model = User
        fields = ["id","nick_name",'image','category','org','org_name']
class UserInfoShowSerializer(serializers.ModelSerializer):
    '''用于公共展示教师或者学生信息'''
    org_name=serializers.ReadOnlyField(source='org.name')
    class Meta:
        model = User
        fields = ["id","nick_name", "gender",'self_introduction',
                   "email",'image','category','org','org_name']