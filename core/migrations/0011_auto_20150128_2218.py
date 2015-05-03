# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_auto_20141216_0236'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='color',
            field=models.CharField(max_length=18, null=True,
                                   choices=[(b'#20F606', b'#20F606'),
                                            (b'#24AEFF', b'#24AEFF'),
                                            (b'#610081', b'#610081'),
                                            (b'#EE9A28', b'#EE9A28'),
                                            (b'#C8B02A', b'#C8B02A'),
                                            (b'#A34B0A', b'#A34B0A'),
                                            (b'#F0FD39', b'#F0FD39'),
                                            (b'#F0C0C1', b'#F0C0C1'),
                                            (b'#C8005D', b'#C8005D'),
                                            (b'#EFD276', b'#EFD276'),
                                            (b'#596468', b'#596468'),
                                            (b'#EC2809', b'#EC2809'),
                                            (b'#000000', b'#000000'),
                                            (b'#FDC50B', b'#FDC50B'),
                                            (b'#149E9C', b'#149E9C'),
                                            (b'#0000FF', b'#0000FF'),
                                            (b'#D900CC', b'#D900CC'),
                                            (b'#90C423', b'#90C423'),
                                            (b'#5FFEEE', b'#5FFEEE'),
                                            (b'#D464F0', b'#D464F0'),
                                            (b'#C2CCDF', b'#C2CCDF'),
                                            (b'#FD8609', b'#FD8609'),
                                            (b'#18930B', b'#18930B'),
                                            (b'#FB0007', b'#FB0007')]),
            preserve_default=True,
        ),
    ]
