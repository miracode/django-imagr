# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('imagr', '0005_auto_20141105_1254'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='imagruser',
            name='followers',
        ),
    ]
