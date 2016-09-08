# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import localflavor.us.models


class Migration(migrations.Migration):

    dependencies = [
        ('pharmacist', '0009_auto_20160908_2021'),
    ]

    operations = [
        migrations.AddField(
            model_name='patient',
            name='ssn',
            field=localflavor.us.models.USSocialSecurityNumberField(null=True),
        ),
    ]
