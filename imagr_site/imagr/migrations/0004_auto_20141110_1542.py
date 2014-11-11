# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('imagr', '0003_auto_20141110_1314'),
    ]

    operations = [
        migrations.AlterField(
            model_name='album',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime(2014, 11, 10, 23, 42, 5, 380978, tzinfo=utc), verbose_name=b'date created'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='photo',
            name='file_size',
            field=models.DecimalField(null=True, verbose_name=b'File Size (MB)', max_digits=6, decimal_places=3, blank=True),
            preserve_default=True,
        ),
    ]
