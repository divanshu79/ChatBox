# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0004_user_data'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user_data',
            name='email',
            field=models.CharField(max_length=250),
        ),
    ]
