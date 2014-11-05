# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('imagr', '0008_imagruser_date_joined'),
    ]

    operations = [
        migrations.AlterField(
            model_name='album',
            name='cover_photo',
            field=models.ForeignKey(related_name='cover_photo', blank=True, to='imagr.Photo', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='album',
            name='date_modified',
            field=models.DateTimeField(null=True, verbose_name=b'date modified', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='album',
            name='date_published',
            field=models.DateTimeField(null=True, verbose_name=b'date published', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='album',
            name='description',
            field=models.CharField(max_length=2000, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='album',
            name='photos',
            field=models.ManyToManyField(to='imagr.Photo', null=True, verbose_name=b'photos in album', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='imagruser',
            name='date_joined',
            field=models.DateTimeField(default=datetime.datetime(2014, 11, 5, 22, 36, 31, 349870, tzinfo=utc), verbose_name=b'date joined'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='photo',
            name='date_modified',
            field=models.DateTimeField(null=True, verbose_name=b'date modified', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='photo',
            name='date_published',
            field=models.DateTimeField(null=True, verbose_name=b'date published', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='photo',
            name='description',
            field=models.CharField(max_length=2000, null=True, blank=True),
            preserve_default=True,
        ),
    ]
