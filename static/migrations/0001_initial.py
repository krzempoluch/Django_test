# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MWD',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(max_length=200)),
                ('issue_date', models.DateTimeField(verbose_name='data rozpoczecia dzialania MWD')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Projekt',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(max_length=200)),
                ('jira_URL', models.CharField(max_length=200)),
                ('start_date', models.DateTimeField(verbose_name='data startu')),
                ('mwds', models.ManyToManyField(to='projekty.MWD')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
