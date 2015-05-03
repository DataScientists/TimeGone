# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_trackedtime'),
    ]

    operations = [
        migrations.AddField(
            model_name='trackedtime',
            name='activity',
            field=models.CharField(default=b'', max_length=255),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='trackedtime',
            name='hours',
            field=models.FloatField(
                validators=[django.core.validators.MinValueValidator(0)]),
            preserve_default=True,
        ),
    ]
