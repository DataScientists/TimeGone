# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_trackedtime_manual_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='color',
            field=models.CharField(max_length=7,
                                   null=True,
                                   choices=[(b'#FF9500', b'#FF9500'),
                                            (b'#FF3B30', b'#FF3B30'),
                                            (b'#4CD964', b'#4CD964'),
                                            (b'#FFCC00', b'#FFCC00'),
                                            (b'#BDBEC2', b'#BDBEC2'),
                                            (b'#1F1F21', b'#1F1F21'),
                                            (b'#FF2D55', b'#FF2D55'),
                                            (b'#5856D6', b'#5856D6'),
                                            (b'#007AFF', b'#007AFF'),
                                            (b'#34AADC', b'#34AADC')]),
            preserve_default=True,
        ),
    ]
