# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'location',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Measure',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('value', models.FloatField()),
                ('year', models.IntegerField()),
                ('month', models.IntegerField()),
                ('metrics', models.IntegerField(choices=[(1, b'RAINFALL'), (2, b'TMAX'), (3, b'TMIN')])),
                ('location', models.ForeignKey(to='weather.Location')),
            ],
            options={
                'db_table': 'measure',
            },
            bases=(models.Model,),
        ),
    ]
