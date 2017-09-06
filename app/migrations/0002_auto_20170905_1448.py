# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-05 18:48
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entry',
            name='month',
            field=models.ForeignKey(db_column='month_id', on_delete=django.db.models.deletion.CASCADE, related_name='entries', to='app.Month'),
        ),
    ]