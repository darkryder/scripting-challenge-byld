# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('byld', '0004_question_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='last_question_solved',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
