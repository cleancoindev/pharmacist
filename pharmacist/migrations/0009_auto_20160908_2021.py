# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pharmacist', '0008_emailtracking'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emailtracking',
            name='state',
            field=models.CharField(default=b'sent', max_length=20, choices=[(b'sent', b'email sent'), (b'clicked', b'link clicked'), (b'scheduled', b'appointment scheduled')]),
        ),
    ]
