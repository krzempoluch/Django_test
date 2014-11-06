# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projekty', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='projekt',
            name='MWDs',
        ),
        migrations.AddField(
            model_name='projekt',
            name='Dupa',
            field=models.ManyToManyField(to='projekty.MWD'),
            preserve_default=True,
        ),
    ]
