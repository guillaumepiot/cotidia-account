# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-12-22 15:57
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_auto_20170623_1651'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'ordering': ['first_name', 'last_name'], 'verbose_name': 'User', 'verbose_name_plural': 'Users'},
        ),
    ]
