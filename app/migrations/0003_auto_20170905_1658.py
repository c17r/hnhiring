# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-05 20:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20170905_1448'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entry',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='month',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
