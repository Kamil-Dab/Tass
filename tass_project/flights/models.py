from django.db import models

from cities.models import City


class Airport(models.Model):
    code = models.PositiveIntegerField(unique=True,null=False, blank=False)
    description = models.CharField(max_length=100)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, blank=True)
    city_description = models.CharField(max_length=100, blank=True)
    lat = models.FloatField(null=True)
    lng = models.FloatField(null=True)
    country_code = models.CharField(max_length=2, blank=True)
    state_code = models.CharField(max_length=2, blank=True)
    
    def __str__(self):
        return self.description

class Flight(models.Model):
    itin_id = models.PositiveBigIntegerField(null=False, blank=False)
    mkt_id = models.PositiveBigIntegerField(null=False, blank=False)
    quarter = models.PositiveIntegerField(null=False, blank=False)
    origin_airport = models.ForeignKey(Airport, to_field="code", on_delete=models.CASCADE, related_name="origin_airport")
    dest_airport = models.ForeignKey(Airport, to_field="code", on_delete=models.CASCADE, related_name="destination_airport")
    passengers = models.PositiveIntegerField(null=False, blank=False)
    distance = models.PositiveIntegerField(null=False, blank=False)

    def __str__(self):
        return str(self.itin_id)
