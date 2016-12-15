# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2016-12-10 02:36
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('availability', models.BooleanField(default=True)),
                ('profile_pic', models.ImageField(upload_to=b'')),
            ],
        ),
        migrations.CreateModel(
            name='Pair',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('employee_one', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='employee_one', to='pairs.Employee')),
                ('employee_two', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='employee_two', to='pairs.Employee')),
            ],
        ),
        migrations.CreateModel(
            name='PairCall',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_done', models.BooleanField(default=False)),
                ('date', models.DateField()),
                ('picture', models.ImageField(upload_to=b'')),
                ('caption', models.CharField(max_length=400)),
                ('pair', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pairs.Pair')),
            ],
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.AddField(
            model_name='employee',
            name='team',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pairs.Team'),
        ),
    ]
