# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={},
        ),
        migrations.AddField(
            model_name='user',
            name='company_name',
            field=models.CharField(max_length=100, null=True, verbose_name=b'Company name', blank=True),
        ),
        migrations.AddField(
            model_name='user',
            name='fax_number',
            field=models.CharField(max_length=100, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='user',
            name='mobile_number',
            field=models.CharField(max_length=100, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='user',
            name='phone_number',
            field=models.CharField(max_length=100, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='user',
            name='special_instructions',
            field=models.TextField(max_length=1000, null=True, verbose_name=b'Special instructions', blank=True),
        ),
        migrations.AddField(
            model_name='user',
            name='title',
            field=models.CharField(blank=True, max_length=100, null=True, choices=[(b'', b'---'), (b'mr', b'Mr'), (b'mrs', b'Mrs'), (b'ms', b'Ms'), (b'miss', b'Miss'), (b'dr', b'Dr'), (b'prof', b'Prof'), (b'rev', b'Rev'), (b'sir', b'Sir')]),
        ),
        migrations.AlterModelTable(
            name='user',
            table='account_user',
        ),
    ]
