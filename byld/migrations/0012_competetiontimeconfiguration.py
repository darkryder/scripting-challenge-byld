# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('byld', '0011_team_atm_balance'),
    ]

    operations = [
        migrations.CreateModel(
            name='CompetetionTimeConfiguration',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('GAMEDATE', models.DateTimeField()),
                ('GAMEEND', models.DateTimeField()),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
