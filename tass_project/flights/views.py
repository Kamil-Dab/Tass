import json

from django.views.generic import TemplateView
from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework.response import Response

from cities.models import City
from cities.serializers import CitySerializer


class MapView(TemplateView):
    template_name = "interactive_map/main.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["top_cities"] = City.objects.all().order_by("rating")[:50]
        context["max_population"] = City.objects.all().order_by("-population").first().population
        return context


class CityView(APIView):
    def get(self, request: Request):
        query = request.query_params.get("query")
        population = json.loads(request.query_params.get("population"))
        rating = json.loads(request.query_params.get("rating"))
        filters = {
            "population__range": population,
            "rating__range": rating,
        }
        if query:
            filters["city__icontains"] = query
        return Response(CitySerializer(City.objects.filter(**filters), many=True).data[:100])


class CityRatingView(APIView):
    "Retrieve only rating values with latlng for heat map"

    def get(self, request: Request):
        return Response(list(City.objects.values("lat", "lng", "rating")))
