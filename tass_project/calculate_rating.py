import django
from django.db.models import Count, Sum, F
django.setup()

from flights.models import Flight
from cities.models import City


def calculate_rating():
    counted_cities = Flight.objects.filter(dest_airport__city__isnull=False)\
                                    .values("dest_airport__city__pk")\
                                    .order_by("pk")\
                                    .annotate(city_id=F("dest_airport__city__pk"),
                                              flights_count=Count("dest_airport__city__pk"),
                                              passengers_sum=Sum("passengers"))\
                                    .values("city_id", "flights_count", "passengers_sum")\
                                    .order_by("-passengers_sum")
    cities = []
    max_rating = 0
    City.objects.all().update(rating=0.0)
    for city_values in counted_cities:
        city = City.objects.get(pk=city_values["city_id"])
        ratio_pass_sum = city_values["passengers_sum"] / city.population
        ratio_flights_count = city_values["flights_count"] / city.population
        city.rating = ratio_pass_sum + ratio_flights_count
        if city.rating > max_rating:
            max_rating = city.rating
        cities.append(city)
    for city in cities:
        city.rating = round(city.rating / max_rating * 10, 1)
    City.objects.bulk_update(cities, ["rating"])

if __name__ == '__main__':
    calculate_rating()
