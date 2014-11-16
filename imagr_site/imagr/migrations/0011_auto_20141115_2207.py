# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('imagr', '0010_auto_20141114_1705'),
    ]

    operations = [
        migrations.AlterField(
            model_name='album',
            name='photos',
            field=models.ManyToManyField(to='imagr.Photo', null=True, verbose_name=b'photos in album', blank=True),
            preserve_default=True,
        ),
    ]
