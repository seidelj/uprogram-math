# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mathtutor', '0009_parentformresult'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quiz',
            name='site',
            field=models.CharField(default=b'math', max_length=16, verbose_name=b'Website'),
        ),
    ]
