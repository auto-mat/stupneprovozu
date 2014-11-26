# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Lokace',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Provoz',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ident', models.IntegerField()),
                ('level', models.IntegerField()),
                ('time_generated', models.DateTimeField()),
                ('time_start', models.DateTimeField()),
                ('time_stop', models.DateTimeField()),
                ('location', models.ForeignKey(to='tsk.Lokace')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
