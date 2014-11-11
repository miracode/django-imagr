# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('imagr', '0006_auto_20141111_1324'),
    ]

    operations = [
        migrations.AlterField(
            model_name='album',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime(2014, 11, 11, 23, 5, 43, 659018, tzinfo=utc), verbose_name=b'date created'),
            preserve_default=True,
        ),
    ]
