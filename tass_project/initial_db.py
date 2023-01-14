import django
from tqdm import tqdm
django.setup()

import pandas as pd
from flights.models import Airport, Flight
from cities.models import City


print("import cities")
records = pd.read_csv("./data/city.csv", sep=",").fillna("").to_dict("records")
cities = []
for record in tqdm(records):
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
City.objects.bulk_create(cities)
print("import cities done")

print("import airports")
records = pd.read_csv("./data/T_MASTER_CORD.csv", sep=",").fillna("")
records = records.drop_duplicates(subset='AIRPORT_ID', keep="last").to_dict("records")
airports = []
cities = {(city.city, city.state_id): city for city in City.objects.all()}
for record in tqdm(records):
    if int(record["AIRPORT_ID"]) == 99999:
        continue
    description = f"{record['DISPLAY_AIRPORT_CITY_NAME_FULL']}: {record['DISPLAY_AIRPORT_NAME']}"
    city_name = record["DISPLAY_AIRPORT_CITY_NAME_FULL"].split(",")[0].strip()
    city_state = record["DISPLAY_AIRPORT_CITY_NAME_FULL"].split(",")[1].strip()
    city = City.objects.filter(city=city_name, state_id=city_state)
    if city.exists():
        city = city.first()
    else:
        city = None
    airport = Airport(
        code=int(record["AIRPORT_ID"]),
        lat = record["LATITUDE"],
        lng = record["LONGITUDE"],
        description = description,
        city_description = record["DISPLAY_AIRPORT_CITY_NAME_FULL"],
        state_code = record["AIRPORT_STATE_CODE"],
        country_code = record["AIRPORT_COUNTRY_CODE_ISO"],
        city = city
    )
    airports.append(airport)
Airport.objects.bulk_create(airports)
print("import airport done")

print("import flights")
limit_bulk = 1000000 # create partially because of memory
airports = {airport.code: airport for airport in Airport.objects.all()}
flights = []
with pd.read_csv("./data/flights.csv", sep=",", chunksize=1000000) as reader:
    counter = 1
    for chunk in reader:
        records = chunk.fillna("").to_dict("records")
        for i, record in tqdm(enumerate(records)):
            flights.append(Flight(
                itin_id=record["ItinID"],
                mkt_id=record["MktID"],
                quarter=record["Quarter"],
                origin_airport=airports[int(record["OriginAirportID"])],
                dest_airport=airports[int(record["DestAirportID"])],
                passengers=int(float(record["Passengers"])),
                distance=int(float(record["MktDistance"])),
            ))
            if len(flights) == limit_bulk:
                Flight.objects.bulk_create(flights)
                print(f"Created {(i+1) * counter} records")
                flights = []
        counter += 1
    Flight.objects.bulk_create(flights)
print("import flights done")
