# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('byld', '0002_gamestatus'),
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('description', models.CharField(default=b'', max_length=100, blank=True)),
                ('hash', models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('description', models.CharField(max_length=1024)),
                ('points', models.IntegerField(default=0, max_length=1000)),
            ],
        ),
        migrations.RemoveField(
            model_name='gamestatus',
            name='team',
        ),
        migrations.AlterField(
            model_name='team',
            name='score',
            field=models.IntegerField(default=0),
        ),
        migrations.DeleteModel(
            name='GameStatus',
        ),
        migrations.AddField(
            model_name='question',
            name='solved_by',
            field=models.ManyToManyField(related_name='solved_questions', to='byld.Team'),
        ),
        migrations.AddField(
            model_name='answer',
            name='question',
            field=models.ForeignKey(related_name='answers', to='byld.Question'),
        ),
    ]
