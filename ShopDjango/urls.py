"""ShopDjango URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
# from django.contrib import admin
from rest_framework_jwt.views import obtain_jwt_token

import xadmin
from ShopDjango.settings import MEDIA_ROOT
from django.views.static import serve
from rest_framework.documentation import include_docs_urls
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views

from goods.views import GoodsListViewSet, GoodsCategoryListViewSet, HotSearchWordsListViewSet, \
    SearchPriceRangeListViewSet, BannerViewSet, NewGoodsViewSet, IndexCategoryGoodsViewSet
from users.views import SmsCodeViewSet, UserViewSet
from user_operation.views import UserFavViewSet, UserLeavingMessageViewSet, UserAddressViewSet
from trade.views import ShoppingCartViewSet, OrderInfoVewSet


router = DefaultRouter()
# 配置goods的url
router.register(r'goods', GoodsListViewSet, base_name='goods')
# 配置categorys的url
router.register(r'goodsCategorys', GoodsCategoryListViewSet)
# 配置hotsearchs的url
router.register(r'hotsearchs', HotSearchWordsListViewSet)
# 配置searchpricerange的url
router.register(r'priceRange', SearchPriceRangeListViewSet)
# 配置发送验证码接口
router.register(r'smscodes', SmsCodeViewSet, base_name='smscodes')
# 用户
router.register(r'users', UserViewSet, base_name='users')
# 用户收藏
router.register(r'userfavs', UserFavViewSet, base_name='userfavs')
# 用户留言
router.register(r'messages', UserLeavingMessageViewSet, base_name='messages')
# 收货地址
router.register(r'address', UserAddressViewSet, base_name='address')
# 购物车
router.register(r'shopcarts', ShoppingCartViewSet, base_name='shopcarts')
# 订单
router.register(r'orders', OrderInfoVewSet, base_name='orders')
# 首页轮播图
router.register(r'banners', BannerViewSet, base_name='banners')
# 新鲜出炉
router.register(r'newgoods', NewGoodsViewSet, base_name='newgoods')
# 首页分类
router.register(r'indexgoods', IndexCategoryGoodsViewSet, base_name='indexgoods')

# goods_list = GoodsListViewSet.as_view({
#     'get': 'list'
# })

urlpatterns = [
    # 后台路径
    url(r'^xadmin/', xadmin.site.urls),
    # api登录路径
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    # drf自带auth token认证模式
    url(r'^api-token-auth', views.obtain_auth_token),
    # jwt认证接口
    url(r'^login', obtain_jwt_token),
    # 媒体文件路径
    url(r'^media/(?P<path>.*)$', serve, {"document_root": MEDIA_ROOT}),
    #
    url(r'^', include(router.urls)),

    # 商品列表页
    # url(r'goods/$', goods_list, name="goods-list"),

    # 文档路径
    url(r'docs/', include_docs_urls(title='生鲜网'))
]
