# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mathtutor', '0006_auto_20150929_0722'),
    ]

    operations = [
        migrations.AddField(
            model_name='quiz',
            name='site',
            field=models.CharField(default=b'tutor', max_length=16, verbose_name=b'Website'),
        ),
    ]
