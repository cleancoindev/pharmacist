# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pharmacist', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Medication',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('med_id', models.IntegerField(unique=True)),
                ('name', models.CharField(max_length=255)),
                ('pharmacy_note', models.CharField(max_length=1024)),
                ('rxnorm', models.CharField(max_length=255)),
                ('number_refills', models.IntegerField()),
            ],
        ),
        migrations.RemoveField(
            model_name='doctor',
            name='user',
        ),
        migrations.RemoveField(
            model_name='patient',
            name='user',
        ),
        migrations.AddField(
            model_name='doctor',
            name='doctor_id',
            field=models.IntegerField(default=None, unique=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='patient',
            name='patient_id',
            field=models.IntegerField(default=None, unique=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='doctor',
            name='id',
            field=models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True),
        ),
        migrations.AlterField(
            model_name='patient',
            name='doctor',
            field=models.ForeignKey(to='pharmacist.Doctor'),
        ),
        migrations.AlterField(
            model_name='patient',
            name='id',
            field=models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True),
        ),
        migrations.AddField(
            model_name='medication',
            name='doctor',
            field=models.ForeignKey(to='pharmacist.Doctor'),
        ),
        migrations.AddField(
            model_name='medication',
            name='patient',
            field=models.ForeignKey(to='pharmacist.Patient'),
        ),
    ]
