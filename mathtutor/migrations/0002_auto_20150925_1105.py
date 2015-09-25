# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mathtutor', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='theme',
            field=models.OneToOneField(null=True, blank=True, to='mathtutor.Themes'),
        ),
    ]
