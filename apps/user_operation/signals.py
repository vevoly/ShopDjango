# _*_ coding: utf-8 _*_

__author__ = 'jevoly'
__date__ = '2018/12/22 0022 下午 8:44'

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from .models import UserFav


@receiver(post_save, sender=UserFav)
def create_fav(sender, instance=None, created=False, **kwargs):
    if created:
        goods = instance.goods
        goods.fav_num += 1
        goods.save()
        instance.save()


@receiver(post_delete, sender=UserFav)
def delete_fav(sender, instance=None, created=False, **kwargs):
    goods = instance.goods
    goods.fav_num -= 1
    goods.save()
