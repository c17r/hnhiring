# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Entry',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('hn_id', models.IntegerField(null=True, blank=True)),
                ('content', models.TextField(blank=True)),
                ('date', models.DateTimeField(blank=True)),
            ],
            options={
                'db_table': 'entry',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Month',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('hn_id', models.IntegerField(null=True, blank=True)),
                ('name', models.TextField(blank=True)),
            ],
            options={
                'db_table': 'month',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='entry',
            name='month',
            field=models.ForeignKey(related_name='entries', db_column='month_id', to='app.Month'),
            preserve_default=True,
        ),
    ]
