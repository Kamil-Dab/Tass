from django.db import models


class Airport(models.Model):
    code = models.PositiveIntegerField(unique=True,null=False, blank=False)
    description = models.CharField(max_length=100)

class Flight(models.Model):
    itin_id = models.PositiveBigIntegerField(null=False, blank=False)
    mkt_id = models.PositiveBigIntegerField(null=False, blank=False)
    quarter = models.PositiveIntegerField(null=False, blank=False)
    origin_airport = models.ForeignKey(Airport, to_field="code", on_delete=models.CASCADE, related_name="origin_airport")
    dest_airport = models.ForeignKey(Airport, to_field="code", on_delete=models.CASCADE, related_name="destination_airport")
    passengers = models.PositiveIntegerField(null=False, blank=False)
    distance = models.PositiveIntegerField(null=False, blank=False)
