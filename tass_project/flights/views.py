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
        return context


class CityView(APIView):
    def get(self, request: Request):
        query = request.query_params.get("query")
        return Response(CitySerializer(City.objects.filter(city__icontains=query), many=True).data)
