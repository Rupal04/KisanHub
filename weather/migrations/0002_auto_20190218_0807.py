# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('weather', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='measure',
            name='metrics',
            field=models.CharField(max_length=50, choices=[(b'Rainfall', b'Rainfall'), (b'Tmax', b'Tmax'), (b'Tmin', b'Tmin')]),
            preserve_default=True,
        ),
    ]
