# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('imagr', '0007_auto_20141105_1304'),
    ]

    operations = [
        migrations.AddField(
            model_name='imagruser',
            name='date_joined',
            field=models.DateTimeField(default=datetime.datetime(2014, 11, 5, 21, 43, 6, 567435, tzinfo=utc), verbose_name=b'date joined'),
            preserve_default=True,
        ),
    ]
