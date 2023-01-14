import json

from django.views.generic import TemplateView
from django.shortcuts import redirect
from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework.response import Response

from cities.models import City
from cities.serializers import CitySerializer
from calculate_rating import calculate_rating


class MapView(TemplateView):
    template_name = "interactive_map/main.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["top_cities"] = City.objects.filter(rating__gt=0.0).order_by("-rating")
        context["max_population"] = City.objects.all().order_by("-population").first().population
        return context

    def get(self, request, *args, **kwargs):
        if "recalculate_rating" in request.GET:
            calculate_rating()
            return redirect('interactive_map')
        return super().get(request, *args, **kwargs)

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
