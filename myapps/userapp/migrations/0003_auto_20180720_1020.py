# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-07-20 02:20
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userapp', '0002_user_token'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'verbose_name': '用户列表', 'verbose_name_plural': '用户列表'},
        ),
        migrations.AlterModelTable(
            name='user',
            table='user_job',
        ),
    ]