# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import mathtutor.models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Consent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('c_child', models.CharField(max_length=256, verbose_name=b"Child's Name")),
                ('c_teacher', models.CharField(max_length=256, verbose_name=b"Child's Teacher")),
                ('c_guardian', models.CharField(max_length=256, verbose_name=b'Name of Parent/Guardian')),
                ('c_timestamp', models.DateTimeField(default=mathtutor.models.get_now, verbose_name=b'Time')),
            ],
        ),
        migrations.CreateModel(
            name='LearnItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('l_category', models.CharField(max_length=8, verbose_name=b'Category')),
                ('l_title', models.CharField(max_length=256, verbose_name=b'Title')),
                ('l_path', models.CharField(max_length=512, verbose_name=b'Path')),
                ('l_image', models.CharField(max_length=256, verbose_name=b'Image Name')),
            ],
        ),
        migrations.CreateModel(
            name='LearnType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=8, verbose_name=b'Type')),
            ],
        ),
        migrations.CreateModel(
            name='Quizes',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('q_id', models.CharField(max_length=256, verbose_name=b'Quiz ID')),
                ('q_name', models.CharField(max_length=256, verbose_name=b'Quiz Name')),
                ('q_catagory', models.CharField(max_length=8, verbose_name=b'Category')),
            ],
        ),
        migrations.CreateModel(
            name='QuizGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('group', models.CharField(max_length=8, verbose_name=b'Group')),
            ],
        ),
        migrations.CreateModel(
            name='Results',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('response_id', models.CharField(max_length=256, verbose_name=b'Response ID')),
                ('score', models.CharField(max_length=16, verbose_name=b'Score')),
                ('finished', models.CharField(max_length=8, verbose_name=b'Finished')),
                ('name', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('quiz', models.ForeignKey(blank=True, to='mathtutor.Quizes', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('group', models.IntegerField(default=0, verbose_name=b'Group')),
                ('treatment', models.CharField(max_length=64, verbose_name=b'Treatment')),
                ('score', models.CharField(max_length=8, verbose_name=b'Test Score')),
                ('percentile', models.CharField(max_length=8, verbose_name=b'Scored Higher')),
                ('theme', models.IntegerField(default=0, verbose_name=b'Theme')),
                ('assent', models.IntegerField(default=0, verbose_name=b'Student Assent')),
                ('consent', models.IntegerField(default=0, verbose_name=b'Parent Consent')),
                ('district', models.CharField(max_length=8, verbose_name=b'District')),
                ('stuid', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='SubCatagory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=256, verbose_name=b'SubCategory')),
            ],
        ),
        migrations.CreateModel(
            name='ThemeInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('number', models.IntegerField(verbose_name=b'Level')),
                ('description', models.CharField(max_length=256, verbose_name=b'Level Description')),
                ('image', models.CharField(max_length=256, verbose_name=b'Image File')),
                ('level_tagline', models.CharField(max_length=512, verbose_name=b'Level Tagline')),
                ('article', models.CharField(max_length=128, verbose_name=b'Article')),
            ],
        ),
        migrations.CreateModel(
            name='Themes',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=256, verbose_name=b'Name')),
                ('abbrv', models.CharField(max_length=256, verbose_name=b'Name Abbrevation')),
                ('theme_tagline', models.CharField(max_length=512, verbose_name=b'Theme Tagline')),
                ('your_task', models.CharField(max_length=512, verbose_name=b'Your Task')),
            ],
        ),
        migrations.AddField(
            model_name='themeinfo',
            name='name',
            field=models.ForeignKey(to='mathtutor.Themes'),
        ),
        migrations.AddField(
            model_name='quizes',
            name='q_group',
            field=models.ForeignKey(blank=True, to='mathtutor.QuizGroup', null=True),
        ),
        migrations.AddField(
            model_name='learnitem',
            name='l_group',
            field=models.ForeignKey(blank=True, to='mathtutor.QuizGroup', null=True),
        ),
        migrations.AddField(
            model_name='learnitem',
            name='l_sub',
            field=models.ForeignKey(blank=True, to='mathtutor.SubCatagory', null=True),
        ),
        migrations.AddField(
            model_name='learnitem',
            name='l_type',
            field=models.ForeignKey(blank=True, to='mathtutor.LearnType', null=True),
        ),
    ]
