from random import random

from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.contrib.auth import get_user_model
from django.shortcuts import render
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework import viewsets, status, authentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework_jwt.serializers import jwt_payload_handler, jwt_encode_handler


from utils.strUtlis import generic_code
from .models import VerifyCode
from .serializers import SmsSerializer, UserRegisterSerializer, UserDetailSerializer

# Create your views here.
User = get_user_model()


class CustomBackend(ModelBackend):
    """
    自定义用户验证
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(Q(username=username) | Q(mobile=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class SmsCodeViewSet(CreateModelMixin, viewsets.GenericViewSet):
    """
    发送短信验证码
    """
    serializer_class = SmsSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        mobile = serializer.validated_data['mobile']
        # 生成4位验证码
        code = generic_code()
        # 保存验证码记录
        code_record = VerifyCode(code=code, mobile=mobile)
        code_record.save()
        print("生成验证码成功！（{0}）".format(code))
        return Response({
            "mobile": mobile
        }, status=status.HTTP_201_CREATED)


class UserViewSet(CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, viewsets.GenericViewSet):
    """
    用户
    create: 注册用户
    retrieve: 检索用户
    update: 修改用户
    """
    serializer_class = UserRegisterSerializer
    queryset = User.objects.all()
    # 使用jwt 和 session 验证方式
    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication)

    # 动态permission
    def get_permissions(self):
        if self.action == 'create':
            return []
        elif self.action == 'retrieve':
            return [IsAuthenticated()]
        return []

    # 动态serializer
    def get_serializer_class(self):
        if self.action == 'create':
            return UserRegisterSerializer
        elif self.action == 'retrieve':
            return UserDetailSerializer
        return UserDetailSerializer

    # 返回用户名和token
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # 通过user生成Token
        user = self.perform_create(serializer)
        re_dict = serializer.data
        # 先生成payload
        payload = jwt_payload_handler(user)
        # 生成token
        re_dict['token'] = jwt_encode_handler(payload)
        # 返回name
        re_dict['name'] = user.name if user.name else user.username
        headers = self.get_success_headers(serializer.data)
        return Response(re_dict, status=status.HTTP_201_CREATED, headers=headers)

    def get_object(self):
        # 直接返回登录对象
        return self.request.user

    def perform_create(self, serializer):
        # 保存后返回对象
        return serializer.save()

