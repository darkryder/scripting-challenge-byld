# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('byld', '0010_team_atm_ongoing'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='ATM_balance',
            field=models.IntegerField(default=100000000),
        ),
    ]
