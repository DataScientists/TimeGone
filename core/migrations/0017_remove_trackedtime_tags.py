# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0016_tag'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='trackedtime',
            name='tags',
        ),
    ]
