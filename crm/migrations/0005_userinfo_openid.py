# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-28 04:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0004_auto_20171227_1207'),
    ]

    operations = [
        migrations.AddField(
            model_name='userinfo',
            name='openid',
            field=models.CharField(blank=True, max_length=64, null=True, verbose_name='微信唯一ID'),
        ),
    ]
