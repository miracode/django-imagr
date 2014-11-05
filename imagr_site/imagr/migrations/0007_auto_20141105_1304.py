# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('imagr', '0006_remove_imagruser_followers'),
    ]

    operations = [
        migrations.AlterField(
            model_name='imagruser',
            name='following',
            field=models.ManyToManyField(related_name='followers', null=True, verbose_name=b'People I follow', to='imagr.ImagrUser', blank=True),
            preserve_default=True,
        ),
    ]
