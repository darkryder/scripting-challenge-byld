# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import byld.models


class Migration(migrations.Migration):

    dependencies = [
        ('byld', '0008_auto_20151004_1552'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='token',
            field=models.CharField(default=byld.models.make_auth, max_length=32),
        ),
    ]
