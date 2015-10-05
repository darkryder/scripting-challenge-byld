# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('byld', '0012_competetiontimeconfiguration'),
    ]

    operations = [
        migrations.AlterField(
            model_name='competetiontimeconfiguration',
            name='GAMEDATE',
            field=models.DateTimeField(default=django.utils.timezone.now, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='competetiontimeconfiguration',
            name='GAMEEND',
            field=models.DateTimeField(default=django.utils.timezone.now, null=True, blank=True),
        ),
    ]
