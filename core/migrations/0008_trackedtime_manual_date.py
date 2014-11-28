# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_auto_20141128_2232'),
    ]

    operations = [
        migrations.AddField(
            model_name='trackedtime',
            name='manual_date',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
