# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pharmacist', '0002_auto_20160907_2112'),
    ]

    operations = [
        migrations.RenameField(
            model_name='doctor',
            old_name='doctor_id',
            new_name='item_id',
        ),
        migrations.RenameField(
            model_name='medication',
            old_name='med_id',
            new_name='item_id',
        ),
        migrations.RenameField(
            model_name='patient',
            old_name='patient_id',
            new_name='item_id',
        ),
        migrations.RemoveField(
            model_name='doctor',
            name='cell_phone',
        ),
        migrations.RemoveField(
            model_name='doctor',
            name='home_phone',
        ),
        migrations.RemoveField(
            model_name='doctor',
            name='job_title',
        ),
        migrations.RemoveField(
            model_name='doctor',
            name='office_phone',
        ),
        migrations.RemoveField(
            model_name='doctor',
            name='specialty',
        ),
        migrations.RemoveField(
            model_name='doctor',
            name='suffix',
        ),
    ]
