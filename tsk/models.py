# -*- coding: utf-8 -*-

from django.db import models

class SkupinaLokaci(models.Model):
    name = models.CharField(max_length=255)
    lokace = models.ManyToManyField("Lokace")


class Lokace(models.Model):
    name = models.CharField(max_length=255)
    favourite = models.BooleanField(verbose_name="Oblíbená", default=False)
    class Meta:
        ordering = ['name']
    def __unicode__(self):
        return self.name


class Provoz(models.Model):
    ident = models.CharField(max_length=255)
    level = models.IntegerField()
    location = models.ForeignKey(Lokace)
    level = models.IntegerField()
    time_generated = models.DateTimeField()
    time_start = models.DateTimeField()
    time_stop = models.DateTimeField()
    class Meta:
        ordering = ['time_generated']

