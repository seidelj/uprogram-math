# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('mathtutor', '0004_student_theme'),
    ]

    operations = [
        migrations.CreateModel(
            name='Quiz',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('q_id', models.CharField(max_length=256, verbose_name=b'Quiz ID')),
                ('q_name', models.CharField(max_length=256, verbose_name=b'Quiz Name')),
                ('q_category', models.CharField(max_length=8, verbose_name=b'Category')),
                ('q_group', models.ForeignKey(blank=True, to='mathtutor.QuizGroup', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Result',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('response_id', models.CharField(max_length=256, verbose_name=b'Response ID')),
                ('score', models.CharField(max_length=16, verbose_name=b'Score')),
                ('finished', models.CharField(max_length=8, verbose_name=b'Finished')),
                ('name', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('quiz', models.ForeignKey(blank=True, to='mathtutor.Quiz', null=True)),
            ],
        ),
        migrations.RenameModel(
            old_name='SubCatagory',
            new_name='SubCategory',
        ),
        migrations.RenameModel(
            old_name='Themes',
            new_name='Theme',
        ),
        migrations.RemoveField(
            model_name='quizes',
            name='q_group',
        ),
        migrations.RemoveField(
            model_name='results',
            name='name',
        ),
        migrations.RemoveField(
            model_name='results',
            name='quiz',
        ),
        migrations.RenameField(
            model_name='consent',
            old_name='c_child',
            new_name='child',
        ),
        migrations.RenameField(
            model_name='consent',
            old_name='c_guardian',
            new_name='guardian',
        ),
        migrations.RenameField(
            model_name='consent',
            old_name='c_teacher',
            new_name='teacher',
        ),
        migrations.RenameField(
            model_name='consent',
            old_name='c_timestamp',
            new_name='timestamp',
        ),
        migrations.DeleteModel(
            name='Quizes',
        ),
        migrations.DeleteModel(
            name='Results',
        ),
    ]
