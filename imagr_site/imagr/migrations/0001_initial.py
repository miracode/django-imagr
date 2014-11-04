# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Album',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=140)),
                ('description', models.CharField(max_length=2000)),
                ('date_uploaded', models.DateTimeField(verbose_name=b'date uploaded')),
                ('date_modified', models.DateTimeField(verbose_name=b'date modified')),
                ('date_published', models.DateTimeField(verbose_name=b'date published')),
                ('published', models.CharField(max_length=8, choices=[(b'private', b'This is private'), (b'shared', b'This is shared'), (b'public', b'This is public')])),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ImagrUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(default=django.utils.timezone.now, verbose_name='last login')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=140)),
                ('description', models.CharField(max_length=2000)),
                ('date_uploaded', models.DateTimeField(verbose_name=b'date uploaded')),
                ('date_modified', models.DateTimeField(verbose_name=b'date modified')),
                ('date_published', models.DateTimeField(verbose_name=b'date published')),
                ('published', models.CharField(max_length=8, choices=[(b'private', b'This is private'), (b'shared', b'This is shared'), (b'public', b'This is public')])),
                ('owner', models.ForeignKey(verbose_name=b'Owner of photo', to='imagr.ImagrUser')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='album',
            name='cover_photo',
            field=models.ForeignKey(related_name='cover_photo', to='imagr.Photo'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='album',
            name='owner',
            field=models.ForeignKey(verbose_name=b'Owner of album', to='imagr.ImagrUser'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='album',
            name='photos',
            field=models.ManyToManyField(to='imagr.Photo', verbose_name=b'photos in album'),
            preserve_default=True,
        ),
    ]
