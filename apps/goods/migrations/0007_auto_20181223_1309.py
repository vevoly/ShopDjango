# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-12-23 13:09
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0006_auto_20181222_2053'),
    ]

    operations = [
        migrations.AlterField(
            model_name='goodsimage',
            name='goods',
            field=models.ForeignKey(help_text='商品', on_delete=django.db.models.deletion.CASCADE, related_name='images', to='goods.Goods', verbose_name='商品'),
        ),
    ]
