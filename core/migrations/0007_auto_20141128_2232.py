# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import timezone_field.fields


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_timezone'),
    ]

    operations = [
        migrations.AddField(
            model_name='trackedtime',
            name='track_date',
            field=models.DateField(null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='timezone',
            name='timezone',
            field=timezone_field.fields.TimeZoneField(
                default=b'Europe/London'),
            preserve_default=True,
        ),
    ]
