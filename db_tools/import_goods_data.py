import sys
import os

# 获取当前文件的所在文件夹
currentDir = os.path.dirname(__file__)
# 将项目根目录追加到path里
sys.path.append(currentDir + "../")
# print(sys.path)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ShopDjango.settings')

import django
django.setup()

from goods.models import Goods, GoodsCategory, GoodsImage
from db_tools.data.product_data import row_data

for product in row_data:
    goods = Goods()
    goods.name = product.get('name')
    goods.market_price = float(int(product.get('market_price').replace("￥", "").replace("元", "")))
    goods.shop_price = float(int(product.get('sale_price').replace("￥", "").replace("元", "")))
    goods.goods_brief = product.get('desc') if product.get('desc') is not None else ""
    goods.goods_desc = product.get('goods_desc') if product.get('goods_desc') is not None else ""
    goods.goods_front_image = product.get('images')[0] if product.get('images') else ""
    goodsImages = product.get('images')
    category_name = product.get('categorys')[-1]
    # objects.filter会获取一个集合
    category = GoodsCategory.objects.filter(name=category_name)
    if category:
        goods.category = category[0]
    print(goods)
    goods.save()

    print('-------images------')
    for imgUrl in product.get('images'):
        image = GoodsImage()
        image.goods = goods
        image.image = imgUrl
        print(image.image)
        image.save()

