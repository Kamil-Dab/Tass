import django
from tqdm import tqdm
django.setup()

import csv
from django.db import transaction

from flights.models import Airport, Flight
from cities.models import City


print("import cities")
with open("./data/city.csv", "r") as file:
    rf = csv.DictReader(file, fieldnames=["custom_id","city","city_ascii","state_id","state_name","lat","lng","population","density","timezone","id"])
    cities = []
    for i, record in tqdm(enumerate(rf)):
        if i ==0:
            continue
        cities.append(City(
            city=record["city"],
            city_ascii=record["city_ascii"],
            state_id=record["state_id"],
            state_name=record["state_name"],
            lat=record["lat"],
            lng=record["lng"],
            population=record["population"],
            density=record["density"],
            timezone=record["timezone"],
            ))
    with transaction.atomic():
        City.objects.bulk_create(cities)
print("import cities done")


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
