
from rest_framework import filters,viewsets,  permissions,exceptions
from .serializers import *
from .models import *
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework.response import Response
from rest_framework.mixins import CreateModelMixin, CreateModelMixin, CreateModelMixin
from random import choice
from mooc1.settings import APIKEY
from rest_framework import serializers, viewsets, status, permissions,mixins
from rest_framework_jwt.serializers import jwt_encode_handler, jwt_payload_handler
from .yunpian import YunPian
from rest_framework.exceptions import ValidationError

User = get_user_model()
class CustomBackend(ModelBackend):
    """
    自定义用户验证，用提供手机号登录
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # user = User.objects.get(Q(username=username))
            user = User.objects.get(Q(username=username) | Q(mobile=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None

class SmsCodeViewSet(CreateModelMixin, viewsets.GenericViewSet):
    """
    发送短信验证码
    """
    #设置序列化类
    serializer_class = SmsSerializer
    #产生随机数
    def generate_code(self):
        """
        生成四位数字的验证码
        :return:
        """
        seeds = "1234567890"
        random_str = []
        for i in range(4):
            random_str.append(choice(seeds))

        return "".join(random_str)
    #重写CreateModelMixin的create方法
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        #这里如果raise_exception设置为True，那么如果序列化过程中发生异常，那么会自动帮我们给客户端返回400异常，比较方便
        serializer.is_valid(raise_exception=True)
        #拿到手机号
        mobile = serializer.validated_data["mobile"]

        yun_pian = YunPian(APIKEY)
        #生产随机验证码
        code = self.generate_code()
        #发送短信
        # sms_status = yun_pian.send_sms(code=code, mobile=mobile)#
        sms_status={"code":0}#暂不发短信
        #云片网的响应，返回0代表成功
        if sms_status["code"] != 0:
            return Response({
                "mobile":sms_status["msg"],

            }, status=status.HTTP_400_BAD_REQUEST)
        else:
            #保存验证码
            code_record = VerifyCode(code=code, mobile=mobile)
            code_record.save()
            return Response({
                "mobile":mobile,
                "code":code#暂时先把验证码返回给浏览器
            }, status=status.HTTP_201_CREATED)


class UserViewSet(CreateModelMixin,mixins.RetrieveModelMixin,mixins.UpdateModelMixin,viewsets.GenericViewSet):
    """
    用户注册，用户详情展示，用户信息修改
    """
    serializer_class = UserRegSerializer

    def get_serializer_class(self):
        if self.action == "retrieve":
            return UserDetailSerializer
        elif self.action == "create":
            return UserRegSerializer

        return UserDetailSerializer
    # permission_classes = (permissions.IsAuthenticated, ) 这样是不行的，因为用户没注册我们不能验证他们权限
    #所以注册和详情的要分开，GenericAPIView->APIView->get_permissions,必须是viewsets.GenericViewSet才有这个功能
    def get_permissions(self):
        if self.action == "retrieve":
            return [permissions.IsAuthenticated()]
        elif self.action == "create":
            return []

        return []
    #create函数在进行注册时，登录后只给我们返回了用户名和Token，并没有给我们用户的id

    def get_object( self ):
        pk=int(self.kwargs.get("pk"))
        if pk:
            if pk != self.request.user.id:
                raise exceptions.PermissionDenied(detail='您无查看此用户详情权限')
            else :return self.request.user
        return self.request.user

    #为什么这里要重写perform_create，因为CreateModelMixin中的perform_create没有return，尽量不修改源码
    def perform_create(self, serializer):
        return serializer.save()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)
        #拿到serializer.data然后将name和token填写进去
        re_dict = serializer.data
        payload = jwt_payload_handler(user)
        re_dict["token"] = jwt_encode_handler(payload)
        # re_dict["name"] = user.name if user.name else user.username
        re_dict["username"] =  user.username
        re_dict["userId"] = user.id
        headers = self.get_success_headers(serializer.data)
        return Response(re_dict, status=status.HTTP_201_CREATED, headers=headers)


class OrganizationViewSet(viewsets.ReadOnlyModelViewSet):#viewsets.ReadOnlyModelViewSet
    queryset = Organization.objects.all().order_by('id')
    serializer_class = OrganizationSerializer

class PasswordUpdateViewSet(mixins.ListModelMixin,mixins.RetrieveModelMixin,mixins.UpdateModelMixin,viewsets.GenericViewSet):#
    """
    登录密码修改
    """
    serializer_class = PasswordUpdateSerializer
    permission_classes = (permissions.IsAuthenticated,)
    def get_permissions(self):
        if self.action == "retrieve":
            return []
        elif self.action == "list":
            raise exceptions.PermissionDenied(detail='您无查看此用户详情权限')
        return []
    def get_object( self ):
        pk = int(self.kwargs.get("pk"))
        if pk:
            if pk != self.request.user.id:
                raise exceptions.PermissionDenied(detail='您无查看此用户详情权限')
            else:
                return self.request.user
        return self.request.user
from django_filters import rest_framework as filters
class UserInfoFilter(filters.FilterSet):
    name = filters.CharFilter(field_name="name", lookup_expr='icontains')
    class Meta:
        model = User
        fields = ['name', 'org','category']
class UserInfoShowViewSet(mixins.ListModelMixin,mixins.RetrieveModelMixin,viewsets.GenericViewSet):
    queryset = User.objects.all().order_by('id')
    serializer_class = UserInfoShowSerializer
    permission_classes = (permissions.IsAuthenticated,)
    filter_class = UserInfoFilter

    def get_serializer_class(self):
        if self.action == "retrieve":
            return UserInfoShowSerializer
        elif self.action == "list":
            return UserInfoListSerializer

        return UserInfoListSerializer