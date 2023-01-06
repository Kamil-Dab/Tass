import django
django.setup()

import csv
from django.db import transaction

from flights.models import DestAirport, OrginAirport, Flights

with transaction.atomic():
    with open("./data/L_AIRPORT_ID.csv", "r") as file:
        rf = csv.DictReader(file, fieldnames=["code","description"])
        for i, record in enumerate(rf):
            if i ==0:
                continue 
            DestAirport.objects.create(code=int(record["code"]),description=record["description"])
            OrginAirport.objects.create(code=int(record["code"]),description=record["description"])

with transaction.atomic():
    with open("./data/flights.csv", "r") as file:
        rf = csv.DictReader(file, fieldnames=["id", "ItinID", "MktID", "Year", "Quarter", "OriginAirportID", "DestAirportID", "Passengers", "MktDistance"])
        for i, record in enumerate(rf):
            if i ==0:
                continue 
            Flights.objects.create(
                itin_id=record["ItinID"],
                mkt_id=record["MktID"],
                quarter=record["Quarter"],
                origin_airport_id=OrginAirport.objects.get(code=int(record["OriginAirportID"])),
                dest_airport_id =DestAirport.objects.get(code=int(record["DestAirportID"])),
                passengers=int(float(record["Passengers"])),
                distance=int(float(record["MktDistance"])),
                )