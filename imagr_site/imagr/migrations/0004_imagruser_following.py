# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('imagr', '0003_auto_20141104_1501'),
    ]

    operations = [
        migrations.AddField(
            model_name='imagruser',
            name='following',
            field=models.ManyToManyField(related_name='following_rel_+', verbose_name=b'Following Users', to='imagr.ImagrUser'),
            preserve_default=True,
        ),
    ]
