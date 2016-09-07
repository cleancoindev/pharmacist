# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pharmacist', '0003_auto_20160907_2218'),
    ]

    operations = [
        migrations.AlterField(
            model_name='medication',
            name='doctor',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='patient',
            name='doctor',
            field=models.IntegerField(),
        ),
        migrations.DeleteModel(
            name='Doctor',
        ),
    ]
