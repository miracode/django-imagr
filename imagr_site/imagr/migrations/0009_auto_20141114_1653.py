# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('imagr', '0008_auto_20141114_1634'),
    ]

    operations = [
        migrations.AlterField(
            model_name='album',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime(2014, 11, 15, 0, 53, 54, 493423, tzinfo=utc), verbose_name=b'date created'),
            preserve_default=True,
        ),
    ]
