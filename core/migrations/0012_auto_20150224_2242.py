# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_auto_20150128_2218'),
    ]

    operations = [
        migrations.RenameField(
            model_name='trackedtime',
            old_name='activity',
            new_name='description',
        ),
    ]
