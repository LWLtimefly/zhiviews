# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-07-20 02:20
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('searchapp', '0002_jobcitys'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='jobcitys',
            options={'managed': False, 'verbose_name': '城市信息', 'verbose_name_plural': '城市信息'},
        ),
        migrations.AlterModelOptions(
            name='jobmsg',
            options={'managed': False, 'verbose_name': '岗位信息详情', 'verbose_name_plural': '岗位信息详情'},
        ),
    ]