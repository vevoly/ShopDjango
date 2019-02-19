# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-11-16 16:15
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trade', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ordergoods',
            name='add_time',
            field=models.DateTimeField(default=datetime.datetime(2018, 11, 17, 0, 15, 46, 99101), help_text='添加时间', verbose_name='添加时间'),
        ),
        migrations.AlterField(
            model_name='orderinfo',
            name='add_time',
            field=models.DateTimeField(default=datetime.datetime(2018, 11, 17, 0, 15, 46, 97101), help_text='添加时间', verbose_name='添加时间'),
        ),
        migrations.AlterField(
            model_name='shoppingcart',
            name='add_time',
            field=models.DateTimeField(default=datetime.datetime(2018, 11, 17, 0, 15, 46, 96101), help_text='添加时间', verbose_name='添加时间'),
        ),
    ]
