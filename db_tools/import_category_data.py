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

#下面的位置非常重要，不能放在上面。因为要先设置django
from goods.models import GoodsCategory

from db_tools.data.category_data import row_data

# 遍历导入数据
for level1 in row_data:
    level1_instance = GoodsCategory()
    level1_instance.name = level1.get("name")
    level1_instance.code = level1.get("code")
    level1_instance.category_type = 1
    level1_instance.save()
    print(level1_instance.name + ", code:" + level1_instance.code)

    for level2 in level1.get("sub_categorys"):
        level2_instance = GoodsCategory()
        level2_instance.name = level2.get("name")
        level2_instance.code = level2.get("code")
        level2_instance.category_type = 2
        level2_instance.parent_category = level1_instance
        level2_instance.save()
        print("------" + level2_instance.name + ", code:" + level2_instance.code + ", parent:" + str(level2_instance.parent_category))

        for level3 in level2.get("sub_categorys"):
            level3_instance = GoodsCategory()
            level3_instance.name = level3.get("name")
            level3_instance.code = level3.get("code")
            level3_instance.category_type = 3
            level3_instance.parent_category = level2_instance
            level3_instance.save()
            print("------------" + level3_instance.name + ", code:" + level3_instance.code + ", parent:" + str(level3_instance.parent_category))



