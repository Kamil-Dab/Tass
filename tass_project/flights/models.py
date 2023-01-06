from django.db import models


class OrginAirport(models.Model):
    code = models.PositiveIntegerField(unique=True,null=False, blank=False)
    description = models.CharField(max_length=100)

class DestAirport(models.Model):
    code = models.PositiveIntegerField(unique=True, null=False, blank=False)
    description = models.CharField(max_length=100)


class Flights(models.Model):
    itin_id = models.PositiveBigIntegerField(null=False, blank=False)
    mkt_id = models.PositiveBigIntegerField(null=False, blank=False)
    quarter = models.PositiveIntegerField(null=False, blank=False)
    origin_airport_id = models.ForeignKey(OrginAirport, to_field="code", on_delete=models.CASCADE)
    dest_airport_id = models.ForeignKey(DestAirport, to_field="code", on_delete=models.CASCADE)
    passengers = models.PositiveIntegerField(null=False, blank=False)
    distance = models.PositiveIntegerField(null=False, blank=False)
