from django.views.generic import TemplateView

from cities.models import City


class MapView(TemplateView):
    template_name = "interactive_map/main.html"

    def get_queryset(self):
        return City.objects.all().order_by("rating")[:50]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["top_cities"] = City.objects.all().order_by("rating")[:50]
        return context
