# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-12-24 12:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_operation', '0006_auto_20181224_1159'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userleavingmessage',
            name='file',
            field=models.FileField(blank=True, help_text='上传的文件', null=True, upload_to='message/image', verbose_name='上传的文件'),
        ),
    ]
