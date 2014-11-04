# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('imagr', '0002_imagruser_identifier'),
    ]

    operations = [
        migrations.AlterField(
            model_name='album',
            name='photos',
            field=models.ManyToManyField(to='imagr.Photo', verbose_name=b'photos in album', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='imagruser',
            name='identifier',
            field=models.CharField(default=b'', unique=True, max_length=40),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='photo',
            name='owner',
            field=models.ForeignKey(related_name='photos', verbose_name=b'Owner of photo', to='imagr.ImagrUser'),
            preserve_default=True,
        ),
    ]
