# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2019-03-10 03:02
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='goods',
            options={'verbose_name': '商品表', 'verbose_name_plural': '商品表'},
        ),
    ]
