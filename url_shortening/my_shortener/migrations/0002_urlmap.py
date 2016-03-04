# -*- coding: utf-8 -*-
# Generated by Django 1.9.3 on 2016-03-03 13:57
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('my_shortener', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UrlMap',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url_actual', models.CharField(max_length=300)),
                ('word', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='my_shortener.Wordlist')),
            ],
        ),
    ]
