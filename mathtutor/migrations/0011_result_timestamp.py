# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import mathtutor.models


class Migration(migrations.Migration):

    dependencies = [
        ('mathtutor', '0010_auto_20160328_1416'),
    ]

    operations = [
        migrations.AddField(
            model_name='result',
            name='timestamp',
            field=models.DateTimeField(default=mathtutor.models.get_now, verbose_name=b'Time Added'),
        ),
    ]
