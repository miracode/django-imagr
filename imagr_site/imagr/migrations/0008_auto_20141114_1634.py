# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('imagr', '0007_auto_20141111_1505'),
    ]

    operations = [
        migrations.AlterField(
            model_name='album',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime(2014, 11, 15, 0, 34, 7, 322366, tzinfo=utc), verbose_name=b'date created'),
            preserve_default=True,
        ),
    ]
