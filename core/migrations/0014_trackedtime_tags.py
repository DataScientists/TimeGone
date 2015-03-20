# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0013_trackedtime_satisfaction'),
    ]

    operations = [
        migrations.AddField(
            model_name='trackedtime',
            name='tags',
            field=models.CharField(default=b'', max_length=255),
            preserve_default=True,
        ),
    ]
