# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-02-14 17:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_legenddata'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContribSourcesByParty',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('interest_category', models.CharField(max_length=200)),
                ('democrat', models.FloatField()),
                ('republican', models.FloatField()),
            ],
        ),
    ]
