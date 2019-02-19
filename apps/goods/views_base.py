from django.views.generic.base import View
# from django.views.generic import ListView

from goods.models import Goods

class GoodsListView(View):

    """
    通过django的view获取商品的列表页
    :param request:
    :return
    """
    def get(self, request):
        json_list = []
        goods = Goods.objects.all()[:10]
        # for good in goods:
        #     json_dict = {}
        #     json_dict['name'] = good.name
        #     json_dict['category'] = good.category.name
        #     json_dict['market_price'] = good.market_price
        #     json_dict['shop_price'] = good.shop_price
        #     json_list.append(json_dict)

        # from django.forms.models import model_to_dict
        # for good in goods:
        #     json_dict = model_to_dict(good)
        #     json_list.append(json_dict)

        import json
        from django.core import serializers
        from django.http import JsonResponse
        json_data = serializers.serialize('json', goods)
        json_data = json.loads(json_data)
        return JsonResponse(json_data, safe=False)





