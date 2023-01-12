from django.views.generic import TemplateView


class MapView(TemplateView):
    template_name = "interactive_map.html"


class RankingView(TemplateView):
    template_name = "ranking.html"

