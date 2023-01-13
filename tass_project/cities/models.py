from django.db import models


class City(models.Model):
    city = models.CharField(max_length=50, null=False, blank=False)
    city_ascii =  models.CharField(max_length=50, null=False, blank=False)
    state_id = models.CharField(max_length=5, null=False, blank=False)
    state_name = models.CharField(max_length=50, null=False, blank=False)
    lat = models.FloatField(null=False, blank=False)
    lng = models.FloatField(null=False, blank=False)
    population = models.PositiveIntegerField(null=False, blank=False)
    density = models.FloatField(null=False, blank=False)
    timezone = models.CharField(max_length=80, null=False, blank=False)
    rating = models.FloatField(default=0.0, null=False, blank=False)
