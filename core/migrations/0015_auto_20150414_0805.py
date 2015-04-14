# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0014_trackedtime_tags'),
    ]

    operations = [
        migrations.AddField(
            model_name='trackedtime',
            name='deleted_project_id',
            field=models.IntegerField(null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='trackedtime',
            name='project',
            field=models.ForeignKey(to='core.Project', null=True),
            preserve_default=True,
        ),
    ]
