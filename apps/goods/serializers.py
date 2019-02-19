from django.db.models import Q
from rest_framework import serializers
# from django.db.models import Q

from .models import Goods, GoodsCategory, HotSearchWords, SearchPriceRange, GoodsImage, Banner, GoodsCategoryBrand, IndexAd


class GoodsImageSerializer(serializers.ModelSerializer):
    """
    商品轮播图
    """
    class Meta:
        model = GoodsImage
        fields = ['image']


class Category3Serializer(serializers.ModelSerializer):
    """
    商品三级分类
    """
    class Meta:
        model = GoodsCategory
        fields = "__all__"


class Category2Serializer(serializers.ModelSerializer):
    """
    商品二级分类
    """
    sub_categorys = Category3Serializer(many=True)
    class Meta:
        model = GoodsCategory
        fields = "__all__"


class CategorySerializer(serializers.ModelSerializer):
    """
    商品分类序列化
    """
    sub_categorys = Category2Serializer(many=True)

    class Meta:
        model = GoodsCategory
        fields = "__all__"


class GoodsSerializer(serializers.ModelSerializer):
    """
    商品序列化
    """
    category = CategorySerializer()
    images = GoodsImageSerializer(many=True)

    class Meta:
        model = Goods
        fields = "__all__"
        # read_only_fields = ('add_time',)
        extra_kwargs = {
            'add_time': {'read_only': True, 'format': '%Y-%m-%d %H:%M'}
        }


class HotSearchWordsSerializer(serializers.ModelSerializer):
    """
    热搜词序列化
    """
    class Meta:
        model = HotSearchWords
        fields = "__all__"


class SearchPriceRangeSerializer(serializers.ModelSerializer):
    """
    搜索价格区间
    """
    class Meta:
        model = SearchPriceRange
        fields = "__all__"


class BannerSerializer(serializers.ModelSerializer):
    """
    轮播图序列化
    """
    class Meta:
        model = Banner
        fields = '__all__'


class GoodsCategoryBrandSerializer(serializers.ModelSerializer):
    """
    商品分类品牌序列化类
    """
    class Meta:
        model = GoodsCategoryBrand
        fields = '__all__'


class IndexAdSerializer(serializers.ModelSerializer):
    """
    广告序列化类
    """
    class Meta:
        model = IndexAd
        fields = '__all__'


class IndexCategoryGoodsSerializer(serializers.ModelSerializer):
    """
    首页商品分类序列化类
    商品一级分类：
    ----显示商品品牌
    ----显示商品二级分类
    ----显示商品
    ----广告
    """
    # 品牌 brands是related_name
    brands = GoodsCategoryBrandSerializer(many=True)
    # 二级分类
    sub_categorys = Category2Serializer(many=True)
    # 商品, 获取一级分类、二级分类、三级分类下所有商品
    goods = serializers.SerializerMethodField()
    # 广告
    ad_goods = serializers.SerializerMethodField()

    def get_ad_goods(self, obj):
        qs = IndexAd.objects.filter(category_id=obj.id)
        qs_json = {}
        if qs:
            goods_ins = qs[0].goods
            serializer = GoodsSerializer(goods_ins, context={'request': self.context['request']})
            qs_json = serializer.data
        return qs_json

    def get_goods(self, obj):
        qs = Goods.objects.filter(Q(category_id=obj.id) | Q(category__parent_category_id=obj.id)
                                  | Q(category__parent_category__parent_category_id=obj.id))
        # 对查询商品进行序列化
        serializer = GoodsSerializer(qs, many=True, context={'request': self.context['request']})
        return serializer.data

    class Meta:
        model = GoodsCategory
        fields = '__all__'
