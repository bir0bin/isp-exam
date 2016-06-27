from __future__ import unicode_literals

from django.db import models


class GcdCache(models.Model):
    a = models.IntegerField(db_index=True)
    b = models.IntegerField(db_index=True)
    data = models.TextField()


class PrimeCache(models.Model):
    n = models.IntegerField(unique=True)
    data = models.TextField()

# Don't care about the code below this line


class Prime(models.Model):
    number = models.IntegerField(unique=True)


class Divisor(models.Model):
    a = models.IntegerField(db_index=True)
    b = models.IntegerField(db_index=True)
    divisor = models.IntegerField()