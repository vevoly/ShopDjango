# _*_ coding: utf-8 _*_


__author__ = 'jevoly'
__date__ = '2018/12/23 0023 下午 1:59'
import re
from rest_framework import serializers

from ShopDjango.settings import REGEX_MOBILE
from .models import UserFav, UserLeavingMessage, UserAddress
from goods.serializers import GoodsSerializer


class UserFavSerializer(serializers.ModelSerializer):
    """
    用户收藏
    """
    # 获取当前登录用户
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = UserFav
        fields = ['user', 'goods', 'id']


class UserFavDetailSerializer(serializers.ModelSerializer):
    """
    用户收藏详情序列化类
    """
    goods = GoodsSerializer()

    class Meta:
        model = UserFav
        fields = ['goods', 'id']


class LeavingMessageSerializer(serializers.ModelSerializer):
    """
    用户留言序列化类
    """
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    add_time = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M')

    class Meta:
        model = UserLeavingMessage
        fields = '__all__'


class UserAddressSerializer(serializers.ModelSerializer):
    """
    用户地址序列化
    """
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    add_time = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M')
    province = serializers.CharField(required=True, max_length=20, help_text='省份')
    city = serializers.CharField(required=True, max_length=20, help_text='城市')
    district = serializers.CharField(required=True, max_length=20, help_text='县/区')
    address = serializers.CharField(required=True, min_length=8, max_length=80, help_text='详细地址')
    signer_name = serializers.CharField(required=True, max_length=20, help_text='签收人姓名')
    signer_mobile = serializers.CharField(max_length=11, label='签收手机号',  help_text='签收人手机号')

    def validate_signer_mobile(self, signer_mobile):
        """
        验证手机号是否合法
        :param signer_mobile: 手机号码
        :return:
        """
        # 验证手机号码是否合法
        if not re.match(REGEX_MOBILE, signer_mobile):
            raise serializers.ValidationError("手机号码非法")
        return signer_mobile

    class Meta:
        model = UserAddress
        fields = '__all__'
