# _*_ coding: utf-8 _*_
from datetime import datetime, timedelta

from rest_framework.validators import UniqueValidator

__author__ = 'jevoly'
__date__ = '2018/12/22 0022 下午 2:51'
import re
from rest_framework import serializers
from django.contrib.auth import get_user_model
from ShopDjango.settings import REGEX_MOBILE

from .models import VerifyCode

User = get_user_model()


class SmsSerializer(serializers.Serializer):
    mobile = serializers.CharField(max_length=11, label='手机号')

    def validate_mobile(self, mobile):
        """
        验证手机号是否合法
        :param mobile: 手机号码
        :return:
        """
        # 手机是否注册
        if User.objects.filter(mobile=mobile).count():
            raise serializers.ValidationError("用户已经存在")
        # 验证手机号码是否合法
        if not re.match(REGEX_MOBILE, mobile):
            raise serializers.ValidationError("手机号码非法")
        # 验证发送频率
        one_min_ago = datetime.now() - timedelta(hours=0, minutes=1, seconds=0)
        if VerifyCode.objects.filter(add_time__gt=one_min_ago, mobile=mobile):
            raise serializers.ValidationError("距上次发送未超过60秒")
        return mobile


class UserRegisterSerializer(serializers.ModelSerializer):
    """
    用户序列化
    """
    # 自定义验证码字段 code
    code = serializers.CharField(max_length=4, min_length=4, help_text='手机验证码', label='手机验证码',
                                 error_messages={
                                     'blank': '请输入验证码',
                                     'required': '请输入验证码',
                                     'max_length': '验证码格式错误',
                                     'min_length': '验证码格式错误'
                                 },
                                 )
    username = serializers.CharField(required=True, allow_blank=False, label='用户名',
                                     # 用户唯一性验证
                                     validators=[UniqueValidator(queryset=User.objects.all(), message='用户已存在')]
                                     )
    password = serializers.CharField(label='密码', help_text='密码',
        style= {
            'input_type': 'password'
        }
    )

    # def create(self, validate_data):
    #     user = super(UserRegisterSerializer, self).create(validated_data=validate_data)
    #     user.set_password(validate_data['password'])
    #     user.save()
    #     return user

    # 验证码验证
    def validate_code(self, code):
        # 取出验证码， inital_data里的内容为前端传过来的原生数据
        codes = VerifyCode.objects.filter(mobile=self.initial_data['username']).order_by('-add_time')
        if not codes:
            raise serializers.ValidationError("请先获取验证码")
        last_code = codes[0]
        # 时间超过5分钟，验证码过期
        five_min_ago = datetime.now() - timedelta(hours=0, minutes=5, seconds=0)
        if last_code.add_time < five_min_ago:
            raise serializers.ValidationError("验证码过期")
        # 比对验证码是否正确
        if not last_code.code == code:
            raise serializers.ValidationError("验证码不正确")

    def validate(self, attrs):
        # attrs是validate后，返回的一个dict
        attrs["mobile"] = attrs["username"]
        del attrs["code"]
        return attrs

    class Meta:
        model = User
        fields = ["username", "code", "password"]
        extra_kwargs = {
            'code': {'write_only': True},
            'password': {'write_only': True}
        }


class UserDetailSerializer(serializers.ModelSerializer):
    """
    用户详情序列化类
    """
    class Meta:
        model = User
        fields = ['name', 'gender', 'birthday', 'email', 'mobile']
