# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-06-26 19:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('initproc', '0013_auto_20170626_1641'),
    ]

    operations = [
        migrations.AddField(
            model_name='proposal',
            name='title',
            field=models.CharField(default='(kein Titel angegeben)', max_length=140),
            preserve_default=False,
        ),
    ]
