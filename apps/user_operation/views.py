from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.mixins import CreateModelMixin, DestroyModelMixin, ListModelMixin, RetrieveModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from .serializers import UserFavSerializer, UserFavDetailSerializer, LeavingMessageSerializer, UserAddressSerializer
from .models import UserFav, UserLeavingMessage, UserAddress
from utils.permissions import IsOwnerOrReadOnly


class UserFavViewSet(viewsets.GenericViewSet, CreateModelMixin, DestroyModelMixin, ListModelMixin, RetrieveModelMixin):
    """
    用户收藏
    list:获取用户收藏列表
    retrieve:判断某个商品是否收藏
    create:收藏商品
    destroy:删除收藏
    """
    serializer_class = UserFavSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    lookup_field = 'goods_id'   # 设置搜索字段 userfavs/1/ <- 就是这个1代表的是goods_id

    # 动态serializer
    def get_serializer_class(self):
        if self.action == 'list':
            return UserFavDetailSerializer
        elif self.action == 'create':
            return UserFavSerializer
        return UserFavSerializer

    def get_queryset(self):
        """
        过滤只能查看自己的收藏列表
        :return:
        """
        return UserFav.objects.filter(user=self.request.user)


class UserLeavingMessageViewSet(CreateModelMixin, ListModelMixin, DestroyModelMixin, viewsets.GenericViewSet):
    """
    用户留言
    create: 新建留言
    list: 列出留言
    delete: 删除留言
    """
    serializer_class = LeavingMessageSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)

    def get_queryset(self):
        """
        过滤只能查看自己的收藏列表
        :return:
        """
        return UserLeavingMessage.objects.filter(user=self.request.user)


class UserAddressViewSet(viewsets.ModelViewSet):
    """
    用户收货地址
    list:       收货地址列表
    retrieve:   收货地址检索
    create:     创建收货地址
    update:     修改收货地址
    delete:     删除收货地址
    """
    serializer_class = UserAddressSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)

    def get_queryset(self):
        return UserAddress.objects.filter(user=self.request.user)

