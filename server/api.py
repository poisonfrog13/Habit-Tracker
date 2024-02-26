from django.urls import path, include

from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
)

from server.apps.habit_tracker import api as habit_tracker_api_endpoints
from server.apps.authentication import api as authentication_api

urlpatterns = []

extra_url_patterns = [
    # Documentation URLs
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "schema/swagger-ui/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    # Include projects API endpoints here
    path("", include(habit_tracker_api_endpoints)),
    path("", include(authentication_api)),
]

urlpatterns += extra_url_patterns