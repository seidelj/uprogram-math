# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('mathtutor', '0008_auto_20160222_1832'),
    ]

    operations = [
        migrations.CreateModel(
            name='ParentFormResult',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('response_id', models.CharField(max_length=256, verbose_name=b'Response ID')),
                ('completeBool', models.IntegerField(default=0, verbose_name=b'Is complete')),
                ('qualtrics_id', models.CharField(max_length=256, verbose_name=b'Qualtrics ID')),
                ('student', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
        ),
    ]
