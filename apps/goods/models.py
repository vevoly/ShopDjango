from datetime import datetime
from django.db import models
from DjangoUeditor.models import UEditorField


class GoodsCategory(models.Model):
    """
    商品分类
    """
    CATEGORY_TYPE = (
        (1, "一级分类"),
        (2, "二级分类"),
        (3, "三级分类"),
    )
    name = models.CharField(default="", max_length=30, verbose_name="类别名", help_text="类别名")
    code = models.CharField(default="", max_length=30, verbose_name="类别code", help_text="类别code")
    desc = models.CharField(default="", max_length=300, verbose_name="类别描述", help_text="类别描述")
    category_type = models.IntegerField(choices=CATEGORY_TYPE, verbose_name="类别类型", help_text="类别类型")
    parent_category = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True, related_name="sub_categorys", verbose_name="父类", help_text="父类别")
    is_tab = models.BooleanField(default=False, verbose_name="是否导航", help_text="是否导航")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间", help_text="添加时间")

    class Meta:
        verbose_name = "商品类别"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class GoodsCategoryBrand(models.Model):
    """
    品牌
    """
    category = models.ForeignKey(GoodsCategory, on_delete=models.CASCADE, verbose_name="商品类目", help_text="商品类目", related_name="brands")
    name = models.CharField(default="", max_length=30, verbose_name="品牌名", help_text="品牌名")
    desc = models.CharField(default="", max_length=30, verbose_name="品牌描述", help_text="品牌描述")
    image = models.ImageField(upload_to = "brands/images/", max_length=200, verbose_name="上传图片", help_text="上传图片")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间", help_text="添加时间")

    class Meta:
        verbose_name = "品牌"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class SearchPriceRange(models.Model):
    """
    分类搜索价格区间
    """
    category = models.ForeignKey(GoodsCategory, on_delete=models.CASCADE, verbose_name="商品类目", help_text="商品类目")
    price_min = models.FloatField(default=0, verbose_name="最小价格", help_text="最小价格")
    price_max = models.FloatField(verbose_name="最大价格", help_text="最大价格")
    index = models.IntegerField(default=0, verbose_name="排序", help_text="排序")

    class Meta:
        verbose_name = "分类搜索价格区间"
        verbose_name_plural = "分类搜索价格区间"

    def __str__(self):
        return "最小值：" + str(self.price_min) + ", 最大值：" + str(self.price_max)


class Goods(models.Model):
    """
    商品
    """
    category = models.ForeignKey(GoodsCategory, on_delete=models.CASCADE, verbose_name="商品类目", help_text="商品类目")
    goods_sn = models.CharField(max_length=50, default="", verbose_name="商品唯一货号", help_text="商品唯一货号")
    name = models.CharField(max_length=100, verbose_name="商品名", help_text="商品名")
    click_num = models.IntegerField(default=0, verbose_name="点击数", help_text="点击数")
    sold_num = models.IntegerField(default=0, verbose_name="销售量", help_text="销售量")
    fav_num = models.IntegerField(default=0, verbose_name="收藏数", help_text="收藏数")
    goods_num = models.IntegerField(default=0, verbose_name="库存数", help_text="库存数")
    market_price = models.FloatField(default=0, verbose_name="市场价格", help_text="市场价格")
    shop_price = models.FloatField(default=0, verbose_name="本店价格", help_text="本店价格")
    goods_brief = models.TextField(max_length=500, verbose_name="商品简短描述", help_text="商品简短描述")
    goods_desc = UEditorField(imagePath="goods/images/", width=1000, height=300, filePath="goods/files/", default="", verbose_name="商品内容", help_text="商品内容")
    ship_free = models.BooleanField(default=True, verbose_name="是否承担运费", help_text="是否承担运费")
    goods_front_image = models.ImageField(upload_to="goods/iamges/", null=True, blank=True, verbose_name="封面图", help_text="封面图")
    is_new = models.BooleanField(default=False, verbose_name="是否新品", help_text="是否新品")
    is_hot = models.BooleanField(default=False, verbose_name="是否热销", help_text="是否热销")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间", help_text="添加时间")

    class Meta:
        verbose_name = "商品"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class GoodsImage(models.Model):
    """
    商品轮播图
    """
    goods = models.ForeignKey(Goods, on_delete=models.CASCADE, verbose_name="商品", help_text="商品", related_name='images')
    image = models.ImageField(upload_to="", verbose_name="图片", null=True, blank=True)
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间", help_text="添加时间")

    class Meta:
        verbose_name = "商品轮播图"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.goods.name


class Banner(models.Model):
    """
    轮播的商品
    """
    goods = models.ForeignKey(Goods, on_delete=models.CASCADE, verbose_name="商品", help_text="商品")
    image = models.ImageField(upload_to="banner", verbose_name="轮播图片", help_text="轮播图片")
    index = models.IntegerField(default=0, verbose_name="轮播排序", help_text="轮播排序")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间", help_text="添加时间")

    class Meta:
        verbose_name = "轮播商品"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.goods.name


class IndexAd(models.Model):
    """
    首页商品类别广告
    """
    category = models.ForeignKey(GoodsCategory, on_delete=models.CASCADE, verbose_name="商品类目")
    goods = models.ForeignKey(Goods, on_delete=models.CASCADE, verbose_name="商品", help_text="商品")

    class Meta:
        verbose_name = "首页商品类别广告"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.goods.name


class HotSearchWords(models.Model):
    """
    热搜词
    """
    keywords = models.CharField(default="", max_length=20, verbose_name="热搜词", help_text="热搜词")
    index = models.IntegerField(default=0, verbose_name="排序", help_text="排序")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间", help_text="添加时间")

    class Meta:
        verbose_name = "热搜词"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.keywords

