# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mathtutor', '0003_remove_student_theme'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='theme',
            field=models.OneToOneField(null=True, blank=True, to='mathtutor.Themes'),
        ),
    ]
