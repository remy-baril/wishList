# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-10-26 19:57
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=500)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('username', models.CharField(max_length=255)),
                ('password', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.AddField(
            model_name='item',
            name='added_by',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='added_items', to='wishBeltApp.User'),
        ),
        migrations.AddField(
            model_name='item',
            name='wished_by',
            field=models.ManyToManyField(default='', related_name='wished_items', to='wishBeltApp.User'),
        ),
    ]
