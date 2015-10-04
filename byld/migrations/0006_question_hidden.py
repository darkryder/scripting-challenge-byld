# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('byld', '0005_team_last_question_solved'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='hidden',
            field=models.BooleanField(default=False),
        ),
    ]
