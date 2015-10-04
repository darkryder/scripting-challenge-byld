# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('byld', '0009_team_token'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='ATM_ongoing',
            field=models.BooleanField(default=False),
        ),
    ]
