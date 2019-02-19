# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-12-04 09:42
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trade', '0002_auto_20181117_0015'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ordergoods',
            name='add_time',
            field=models.DateTimeField(default=datetime.datetime(2018, 12, 4, 9, 42, 7, 110425), help_text='添加时间', verbose_name='添加时间'),
        ),
        migrations.AlterField(
            model_name='orderinfo',
            name='add_time',
            field=models.DateTimeField(default=datetime.datetime(2018, 12, 4, 9, 42, 7, 109425), help_text='添加时间', verbose_name='添加时间'),
        ),
        migrations.AlterField(
            model_name='shoppingcart',
            name='add_time',
            field=models.DateTimeField(default=datetime.datetime(2018, 12, 4, 9, 42, 7, 107425), help_text='添加时间', verbose_name='添加时间'),
        ),
    ]