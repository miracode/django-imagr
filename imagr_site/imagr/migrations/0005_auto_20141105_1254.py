# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('imagr', '0004_imagruser_following'),
    ]

    operations = [
        migrations.AddField(
            model_name='imagruser',
            name='followers',
            field=models.ManyToManyField(related_name='followers_rel_+', null=True, verbose_name=b'People who follow me', to='imagr.ImagrUser', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='album',
            name='cover_photo',
            field=models.ForeignKey(related_name='cover_photo', blank=True, to='imagr.Photo'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='album',
            name='date_modified',
            field=models.DateTimeField(verbose_name=b'date modified', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='album',
            name='date_published',
            field=models.DateTimeField(verbose_name=b'date published', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='album',
            name='description',
            field=models.CharField(max_length=2000, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='imagruser',
            name='following',
            field=models.ManyToManyField(related_name='following_rel_+', null=True, verbose_name=b'People I follow', to='imagr.ImagrUser', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='photo',
            name='date_modified',
            field=models.DateTimeField(verbose_name=b'date modified', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='photo',
            name='date_published',
            field=models.DateTimeField(verbose_name=b'date published', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='photo',
            name='description',
            field=models.CharField(max_length=2000, blank=True),
            preserve_default=True,
        ),
    ]
