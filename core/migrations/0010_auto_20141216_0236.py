# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_project_color'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='color',
            field=models.CharField(
                max_length=18, null=True,
                choices=[(b'rgb(251, 0, 7)', b'rgb(251, 0, 7)'),
                         (b'rgb(240, 192, 193)', b'rgb(240, 192, 193)'),
                         (b'rgb(163, 75, 10)', b'rgb(163, 75, 10)'),
                         (b'rgb(200, 176, 42)', b'rgb(200, 176, 42)'),
                         (b'rgb(32, 246, 6)', b'rgb(32, 246, 6)'),
                         (b'rgb(24, 147, 11)', b'rgb(24, 147, 11)'),
                         (b'rgb(36, 174, 255)', b'rgb(36, 174, 255)'),
                         (b'rgb(20, 158, 156)', b'rgb(20, 158, 156)'),
                         (b'rgb(0, 0, 255)', b'rgb(0, 0, 255)'),
                         (b'rgb(240, 253, 57)', b'rgb(240, 253, 57)'),
                         (b'rgb(144, 196, 35)', b'rgb(144, 196, 35)'),
                         (b'rgb(217, 0, 204)', b'rgb(217, 0, 204)'),
                         (b'rgb(97, 0, 129)', b'rgb(97, 0, 129)'),
                         (b'rgb(200, 0, 93)', b'rgb(200, 0, 93)'),
                         (b'rgb(212, 100, 240)', b'rgb(212, 100, 240)'),
                         (b'rgb(253, 134, 9)', b'rgb(253, 134, 9)'),
                         (b'rgb(236, 40, 9)', b'rgb(236, 40, 9)'),
                         (b'rgb(253, 197, 11)', b'rgb(253, 197, 11)'),
                         (b'rgb(239, 210, 118)', b'rgb(239, 210, 118)'),
                         (b'rgb(238, 154, 40)', b'rgb(238, 154, 40)'),
                         (b'rgb(95, 254, 238)', b'rgb(95, 254, 238)'),
                         (b'rgb(194, 204, 223)', b'rgb(194, 204, 223)'),
                         (b'rgb(89, 100, 104)', b'rgb(89, 100, 104)'),
                         (b'rgb(0, 0, 0)', b'rgb(0, 0, 0)')]),
            preserve_default=True,
        ),
    ]
