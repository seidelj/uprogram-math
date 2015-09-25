# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mathtutor', '0002_auto_20150925_1105'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='theme',
        ),
    ]
