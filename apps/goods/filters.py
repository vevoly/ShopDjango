import django_filters
from django.db.models import Q
from .models import Goods


class GoodsFilter(django_filters.rest_framework.FilterSet):
    """
    商品过滤类
    """
    # 这里的变量名要和前端传值相同
    pricemin = django_filters.NumberFilter(field_name="shop_price", lookup_expr="gte")
    pricemax = django_filters.NumberFilter(field_name="shop_price", lookup_expr="lte")
    top_category = django_filters.NumberFilter(method="top_category_filter", label="顶级分类")
    name = django_filters.CharFilter(field_name="name", lookup_expr="icontains")

    def top_category_filter(self, queryset, name, value):
        """
        查找类别下的所有商品
        商品选择的分类可能是3级分类，也有可能选择2级分类，还可以选择1级分类。
        我们需要满足3种情况：
        1. 如果传值过来的的3级分类，直接category_id=传值
        2. 如果传值过来是2级分类，我们不仅要找出属于2级分类的产品，还要找出2级分类下所属3级分类的产品
        3. 如果传值过来是1级分类，我们不仅要找出所属1级分类产品，还要找出1级分类下所属2级分类、2及分类下所属3级分类的所有产品
        :param queryset:
        :param name:    参数名， 这里会是top_category
        :param value:   参数值
        :return:        过滤结果
        """
        return queryset.filter(Q(category_id=value) | Q(category__parent_category_id=value) | Q(category__parent_category__parent_category_id=value))

    class Meta:
        model = Goods
        fields = ['pricemin', 'pricemax', 'name', 'is_hot', 'is_new']
