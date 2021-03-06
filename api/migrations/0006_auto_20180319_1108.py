# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-03-19 09:08
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_auto_20180227_1620'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='institution',
            options={'managed': False, 'ordering': ('id',)},
        ),
        migrations.AlterModelOptions(
            name='parameter',
            options={'managed': False, 'ordering': ('id',)},
        ),
        migrations.AlterModelOptions(
            name='platform',
            options={'managed': False, 'ordering': ('id',), 'verbose_name_plural': 'platforms'},
        ),
        migrations.AlterModelOptions(
            name='test',
            options={'managed': False, 'ordering': ('-dt',), 'verbose_name_plural': 'Test'},
        ),
    ]
