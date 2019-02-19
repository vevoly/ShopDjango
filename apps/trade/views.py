from django.shortcuts import render

from rest_framework import viewsets
from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from utils.permissions import IsOwnerOrReadOnly
from .serializers import ShoppingCartSerializer, ShoppingCartDetailSerializer, OrderInfoSerializer,\
    OrderInfoDetailSerializer, OrderGoodsSerializer
from .models import ShoppingCart, OrderInfo, OrderGoods


class ShoppingCartViewSet(viewsets.ModelViewSet):
    """
    购物车
    list: 购物车列表
    retrieve: 检索购物车
    create: 新建
    update: 更新
    delete: 删除
    """
    serializer_class = ShoppingCartSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    lookup_field = 'goods_id'

    def get_serializer_class(self):
        if self.action == 'list':
            return ShoppingCartDetailSerializer
        return ShoppingCartSerializer

    def get_queryset(self):
        return ShoppingCart.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        """
        修改商品库存
        goods_num
        :param serializer:
        :return:
        """
        instance = serializer.save()
        goods = instance.goods
        goods.goods_num -= instance.goods_num
        goods.save()

    def perform_update(self, serializer):
        old_record = ShoppingCart.objects.get(id=serializer.instance.id)
        instance = serializer.save()
        goods = instance.goods
        goods.goods_num += (old_record.goods_num - instance.goods_num)
        goods.save()

    def perform_destroy(self, instance):
        goods = instance.goods
        goods.goods_num += instance.goods_num
        goods.save()
        instance.delete()


class OrderInfoVewSet(viewsets.ModelViewSet):
    """
    list: 订单列表
    retrieve: 检索订单
    create: 创建订单
    delete: 删除订单
    """
    serializer_class = OrderInfoSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return OrderInfoDetailSerializer
        return OrderInfoSerializer

    # 只能获取自己的订单
    def get_queryset(self):
        return OrderInfo.objects.filter(user=self.request.user)

    # 重写创建方法
    def perform_create(self, serializer):
        """
        生成订单商品记录
        :param serializer:
        :return:
        """
        order = serializer.save()
        # 取出购物车列表
        shopping_carts = ShoppingCart.objects.filter(user=self.request.user)
        for cart in shopping_carts:
            # 将购物车记录逐条保存到GoodsInfo
            order_goods = OrderGoods()
            order_goods.order = order
            order_goods.goods = cart.goods
            order_goods.goods_num = cart.goods_num
            order_goods.save()
            # 删除购物车商品
            cart.delete()
        return order



