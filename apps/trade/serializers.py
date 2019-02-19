# _*_ coding: utf-8 _*_


__author__ = 'jevoly'
__date__ = '2018/12/24 0024 下午 3:03'

import re
from rest_framework import serializers

from .models import ShoppingCart, OrderInfo, OrderGoods
from goods.models import Goods
from goods.serializers import GoodsSerializer

from ShopDjango.settings import REGEX_MOBILE
from utils import strUtlis


class ShoppingCartSerializer(serializers.Serializer):
    """
    购物车序列化
    """
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    goods_num = serializers.IntegerField(required=True, min_value=1, label="数量", help_text='数量',
                                         error_messages={
                                             'min_value': '商品数量不能小于1',
                                             'required': '请选择购买数量'
                                         })
    # 继承ModelSerializer的话不用指定queryset
    goods = serializers.PrimaryKeyRelatedField(required=True, queryset=Goods.objects.all())

    # 重写新建方法
    def create(self, validated_data):
        user = self.context['request'].user
        goods_nums = validated_data['goods_num']
        goods = validated_data['goods']

        existed = ShoppingCart.objects.filter(user=user, goods=goods)
        if existed:
            existed = existed[0]
            existed.goods_num += goods_nums
            existed.save()
        else:
            existed = ShoppingCart.objects.create(**validated_data)
        return existed

    # 重写更新方法
    def update(self, instance, validated_data):
        # 修改商品数量
        instance.goods_num = validated_data['goods_num']
        instance.save()
        return instance

    # class Meta:
    #     model = ShoppingCart


class ShoppingCartDetailSerializer(serializers.ModelSerializer):
    """
    购物车商品详情序列化类
    """
    goods = GoodsSerializer(many=False)

    class Meta:
        model = ShoppingCart
        fields = '__all__'


class OrderInfoSerializer(serializers.ModelSerializer):
    """
    订单详情序列化类
    """
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    order_sn = serializers.CharField(read_only=True)
    trade_no = serializers.CharField(read_only=True)
    pay_status = serializers.CharField(read_only=True)
    pay_time = serializers.DateTimeField(read_only=True)
    add_time = serializers.DateTimeField(read_only=True)
    singer_mobile = serializers.CharField(max_length=11, label='签收人手机号')

    @staticmethod
    def validate_singer_mobile(singer_mobile):
        """
        验证电话是否合法
        :return:
        """
        if not re.match(REGEX_MOBILE, singer_mobile):
            raise serializers.ValidationError("手机号码不合法")
        else:
            return singer_mobile

    # 重新validate方法，给序列化加入订单号
    def validate(self, attrs):
        """
        加入订单号
        :param attrs:
        :return:
        """
        attrs['order_sn'] = strUtlis.generic_order_sn(self.context['request'].user.id)
        return attrs

    class Meta:
        model = OrderInfo
        fields = '__all__'


class OrderGoodsSerializer(serializers.ModelSerializer):
    """
    订单商品序列化类
    """
    goods = GoodsSerializer(many=False)

    class Meta:
        model = OrderGoods
        fields = '__all__'


class OrderInfoDetailSerializer(serializers.ModelSerializer):
    """
    订单详情序列化类
    """
    goods = OrderGoodsSerializer(many=True)

    class Meta:
        model = OrderInfo
        fields = '__all__'
