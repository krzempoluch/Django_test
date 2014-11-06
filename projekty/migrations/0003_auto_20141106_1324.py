# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projekty', '0002_auto_20141106_1324'),
    ]

    operations = [
        migrations.RenameField(
            model_name='projekt',
            old_name='Dupa',
            new_name='MWDs',
        ),
    ]
