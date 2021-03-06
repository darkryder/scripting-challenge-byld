# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('byld', '0007_auto_20151004_1551'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='solved_by',
            field=models.ManyToManyField(related_name='solved_questions', null=True, to='byld.Team', blank=True),
        ),
    ]
