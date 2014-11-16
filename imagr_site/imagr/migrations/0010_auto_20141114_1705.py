# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('imagr', '0009_auto_20141114_1653'),
    ]

    operations = [
        migrations.AlterField(
            model_name='album',
            name='date_created',
            field=models.DateTimeField(default=datetime.date(2014, 11, 1), verbose_name=b'date created'),
            preserve_default=True,
        ),
    ]
