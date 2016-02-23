# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mathtutor', '0007_quiz_site'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='themeinfo',
            name='name',
        ),
        migrations.RemoveField(
            model_name='student',
            name='theme',
        ),
        migrations.DeleteModel(
            name='Theme',
        ),
        migrations.DeleteModel(
            name='ThemeInfo',
        ),
    ]
