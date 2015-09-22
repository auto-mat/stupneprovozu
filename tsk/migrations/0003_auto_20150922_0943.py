# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tsk', '0002_auto_20141126_1748'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='lokace',
            options={'ordering': ['name']},
        ),
        migrations.AlterModelOptions(
            name='provoz',
            options={'ordering': ['time_generated']},
        ),
        migrations.AddField(
            model_name='lokace',
            name='favourite',
            field=models.BooleanField(default=False, verbose_name=b'Obl\xc3\xadben\xc3\xa1'),
        ),
    ]
