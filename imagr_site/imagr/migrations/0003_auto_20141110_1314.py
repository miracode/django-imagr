# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('imagr', '0002_auto_20141108_1453'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='album',
            name='date_uploaded',
        ),
        migrations.AddField(
            model_name='album',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime(2014, 11, 10, 21, 14, 31, 882546, tzinfo=utc), verbose_name=b'date created'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='photo',
            name='file_size',
            field=models.DecimalField(null=True, max_digits=6, decimal_places=3, blank=True),
            preserve_default=True,
        ),
    ]
