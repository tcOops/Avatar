# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CIUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('alias', models.CharField(max_length=50)),
                ('userId', models.IntegerField()),
                ('name', models.CharField(max_length=50)),
                ('password', models.CharField(max_length=50)),
                ('commit', models.TextField()),
                ('feedbackTime', models.DateField(auto_now_add=True)),
                ('is_deleted', models.BooleanField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Command',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('router_id', models.IntegerField()),
                ('create_time', models.DateField(auto_now_add=True)),
                ('cmd_type', models.CharField(max_length=50)),
                ('params', models.TextField()),
                ('result', models.CharField(max_length=50)),
                ('Is_deleted', models.BooleanField(default=0)),
                ('is_get', models.BooleanField(default=0)),
                ('is_return', models.BooleanField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Routers',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('CIUser_id', models.IntegerField()),
                ('mac_address', models.CharField(max_length=80)),
                ('ip1', models.CharField(max_length=80)),
                ('ip2', models.CharField(max_length=80)),
                ('ip3', models.CharField(max_length=80)),
                ('port', models.IntegerField()),
                ('key', models.CharField(max_length=150)),
                ('method', models.CharField(max_length=150)),
                ('model', models.CharField(max_length=100)),
                ('status', models.CharField(max_length=50)),
                ('update_time', models.DateField(auto_now_add=True)),
                ('is_deleted', models.BooleanField(default=0)),
                ('commit', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('userName', models.CharField(max_length=100)),
                ('password', models.CharField(max_length=100)),
                ('create_time', models.DateField(auto_now_add=True)),
                ('is_deleted', models.BooleanField(default=0)),
            ],
        ),
    ]
