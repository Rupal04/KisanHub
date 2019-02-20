from django.db import models

from weather.constants import Metrics


class Location(models.Model):
    class Meta:
        db_table= "location"

    name = models.CharField(null=False, max_length=100)


class Measure(models.Model):
    class Meta:
        db_table = "measure"

    value = models.FloatField()
    year = models.IntegerField()
    month = models.IntegerField()
    metrics = models.CharField(choices=Metrics, max_length=50)
    location = models.ForeignKey('Location', on_delete=models.CASCADE)


