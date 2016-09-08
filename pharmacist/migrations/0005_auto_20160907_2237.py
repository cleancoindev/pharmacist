# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pharmacist', '0004_auto_20160907_2230'),
    ]

    operations = [
        migrations.AlterField(
            model_name='medication',
            name='doctor',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='medication',
            name='name',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='medication',
            name='number_refills',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='medication',
            name='pharmacy_note',
            field=models.CharField(max_length=1024, null=True),
        ),
        migrations.AlterField(
            model_name='medication',
            name='rxnorm',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='patient',
            name='cell_phone',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='patient',
            name='doctor',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='patient',
            name='email',
            field=models.EmailField(max_length=254, null=True),
        ),
        migrations.AlterField(
            model_name='patient',
            name='first_name',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='patient',
            name='last_name',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='patient',
            name='state',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
