# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2016-08-20 03:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('twitSent', '0011_post_bad'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='tweetContent',
            field=models.CharField(default='', max_length=200),
        ),
    ]