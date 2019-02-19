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

from goods.models import Goods

import json

goods = Goods.objects.all()[:5]
# print(goods[0])
json_list = []
for good in goods:
    json_dict = json.dumps(good)
    print(json_dict)
    json_list.append(json_dict)

print("---------------------------------")
print(json_list)

