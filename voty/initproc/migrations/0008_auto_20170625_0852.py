# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-06-25 08:52
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('initproc', '0007_auto_20170623_1514'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contra',
            name='initiative',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contras', to='initproc.Initiative'),
        ),
        migrations.AlterField(
            model_name='contra',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contras', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='pro',
            name='initiative',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pros', to='initproc.Initiative'),
        ),
        migrations.AlterField(
            model_name='pro',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pros', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='proposal',
            name='initiative',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='proposals', to='initproc.Initiative'),
        ),
        migrations.AlterField(
            model_name='proposal',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='proposals', to=settings.AUTH_USER_MODEL),
        ),
    ]
