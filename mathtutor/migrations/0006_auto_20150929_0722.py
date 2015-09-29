# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mathtutor', '0005_auto_20150928_1545'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='theme',
            field=models.ForeignKey(blank=True, to='mathtutor.Theme', null=True),
        ),
    ]
