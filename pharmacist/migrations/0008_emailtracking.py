# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pharmacist', '0007_auto_20160908_0022'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmailTracking',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('email_hash', models.CharField(unique=True, max_length=255, db_index=True)),
                ('state', models.CharField(max_length=20, choices=[(b'sent', b'email sent'), (b'clicked', b'link clicked'), (b'scheduled', b'appointment scheduled')])),
                ('patient', models.ForeignKey(to='pharmacist.Patient')),
            ],
        ),
    ]
