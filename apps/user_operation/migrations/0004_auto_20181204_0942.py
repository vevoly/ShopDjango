# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-12-04 09:42
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_operation', '0003_auto_20181117_1121'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useraddress',
            name='add_time',
            field=models.DateTimeField(default=datetime.datetime(2018, 12, 4, 9, 42, 7, 105424), help_text='添加时间', verbose_name='添加时间'),
        ),
        migrations.AlterField(
            model_name='userfav',
            name='add_time',
            field=models.DateTimeField(default=datetime.datetime(2018, 12, 4, 9, 42, 7, 103424), help_text='添加时间', verbose_name='添加时间'),
        ),
        migrations.AlterField(
            model_name='userleavingmessage',
            name='add_time',
            field=models.DateTimeField(default=datetime.datetime(2018, 12, 4, 9, 42, 7, 104424), help_text='添加时间', verbose_name='添加时间'),
        ),
    ]
