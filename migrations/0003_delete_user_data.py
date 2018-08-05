# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0002_auto_20180217_1640'),
    ]

    operations = [
        migrations.DeleteModel(
            name='user_data',
        ),
    ]
