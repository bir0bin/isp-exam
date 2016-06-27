# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-06-27 15:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('primeapp', '0002_divisor'),
    ]

    operations = [
        migrations.CreateModel(
            name='GcdCache',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('a', models.IntegerField(db_index=True)),
                ('b', models.IntegerField(db_index=True)),
                ('data', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='PrimeCache',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('n', models.IntegerField(unique=True)),
                ('data', models.TextField()),
            ],
        ),
    ]
