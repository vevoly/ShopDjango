from rest_framework.pagination import PageNumberPagination


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import mixins
from rest_framework import generics
from rest_framework import viewsets
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework_extensions.cache.mixins import CacheResponseMixin
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle

from .models import Goods, GoodsCategory, HotSearchWords, SearchPriceRange, Banner, GoodsCategoryBrand
from .serializers import GoodsSerializer, CategorySerializer, HotSearchWordsSerializer, \
    SearchPriceRangeSerializer, BannerSerializer, IndexCategoryGoodsSerializer
from .filters import GoodsFilter


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 12
    page_size_query_param = 'page_size'
    page_query_param = 'p'
    max_page_size = 100


class GoodsListViewSet(CacheResponseMixin, mixins.ListModelMixin, viewsets.GenericViewSet, mixins.RetrieveModelMixin):
    """
    获取全部商品
    分页、搜索、排序
    """
    queryset = Goods.objects.all()
    serializer_class = GoodsSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filter_class = GoodsFilter
    search_fields = ('name', 'goods_brief', 'goods_desc')
    ordering_fields = ('sold_num', 'shop_price')
    throttle_classes = (AnonRateThrottle, UserRateThrottle)
    # def get_queryset(self):
    #     queryset = Goods.objects.all()
    #     # 设置默认值为0
    #     price_min = self.request.query_params.get("price_min", 0)
    #     if price_min:
    #         queryset = queryset.filter(shop_price__gt=int(price_min))
    #     return queryset

    def retrieve(self, request, *args, **kwargs):
        """
        查看商品详情，商品点击数+1
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        instance = self.get_object()
        instance.click_num += 1
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class GoodsCategoryListViewSet(CacheResponseMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    list:
        商品分类列表数据
    retrieve:
        获取商品分类详情
    """
    queryset = GoodsCategory.objects.filter(category_type=1)
    serializer_class = CategorySerializer
    pagination_class = None

    """
    重写retrieve方法
    解决上面使用filter过滤只能获取1级分类的问题
    """
    def retrieve(self, request, pk):
        instance = GoodsCategory.objects.get(id=pk)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class SearchPriceRangeListViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    根据分类获取搜索价格区间
    """
    queryset = SearchPriceRange.objects.all()
    serializer_class = SearchPriceRangeSerializer
    pagination_class = None
    # 只需要简单的基于等同的过滤，则可以filter_fields在视图或视图集上设置属性，列出要过滤的字段集
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('category_id',)


class HotSearchWordsListViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    热词列表
    """
    queryset = HotSearchWords.objects.order_by("index").all()
    serializer_class = HotSearchWordsSerializer
    ordering_fields = ''
    pagination_class = None


class BannerViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    轮播图
    """
    queryset = Banner.objects.order_by('index').all()
    serializer_class = BannerSerializer


class NewGoodsViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    新鲜出炉
    """
    queryset = Goods.objects.filter(is_new=True).order_by('-add_time')
    serializer_class = GoodsSerializer


class IndexCategoryGoodsViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    首页分类商品
    """
    queryset = GoodsCategory.objects.filter(is_tab=True)
    serializer_class = IndexCategoryGoodsSerializer
