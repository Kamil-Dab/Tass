import django
from tqdm import tqdm
django.setup()

import csv
from django.db import transaction

from flights.models import Airport, Flight


print("import airports")
with open("./data/L_AIRPORT_ID.csv", "r") as file:
    rf = csv.DictReader(file, fieldnames=["code","description"])
    airports = []
    for i, record in tqdm(enumerate(rf)):
        if i ==0:
            continue
        airports.append(Airport(code=int(record["code"]),description=record["description"]))
    with transaction.atomic():
        Airport.objects.bulk_create(airports)
print("import airports done")


limit_bulk = 1000000 # create partially because of memory
print("import flights")
with open("./data/flights.csv", "r") as file:
    rf = csv.DictReader(file, fieldnames=["id", "ItinID", "MktID", "Year", "Quarter","OriginAirportID",
                                            "DestAirportID", "Passengers", "MktDistance"])
    airports = {airport.code: airport for airport in Airport.objects.all()}
    flights = []
    for i, record in tqdm(enumerate(rf)):
        if i == 0:
            continue
        flights.append(Flight(
            itin_id=record["ItinID"],
            mkt_id=record["MktID"],
            quarter=record["Quarter"],
            origin_airport=airports[int(record["OriginAirportID"])],
            dest_airport=airports[int(record["OriginAirportID"])],
            passengers=int(float(record["Passengers"])),
            distance=int(float(record["MktDistance"])),
        ))
        if len(flights) == limit_bulk:
            Flight.objects.bulk_create(flights)
            print(f"Created {i} records")
            flights = []
print("import flights done")
