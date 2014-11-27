from django.db import models

# Create your models here.
class Lokace(models.Model):
    name = models.CharField(max_length=255)
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

