# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-12-20 13:35
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('trade', '0003_auto_20181204_0942'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ordergoods',
            name='add_time',
            field=models.DateTimeField(default=django.utils.timezone.now, help_text='添加时间', verbose_name='添加时间'),
        ),
        migrations.AlterField(
            model_name='orderinfo',
            name='add_time',
            field=models.DateTimeField(default=django.utils.timezone.now, help_text='添加时间', verbose_name='添加时间'),
        ),
        migrations.AlterField(
            model_name='shoppingcart',
            name='add_time',
            field=models.DateTimeField(default=django.utils.timezone.now, help_text='添加时间', verbose_name='添加时间'),
        ),
    ]
