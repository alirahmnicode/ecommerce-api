from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
    SpectacularJSONAPIView,
)
from django.contrib import admin
from django.urls import path, include
import debug_toolbar

from .views import index


admin.site.site_header = "Storefront Admin"
admin.site.index_title = "Admin"


doc_patterns = [
    path('api/schema/yaml/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/json/', SpectacularJSONAPIView.as_view(), name='json-schema'),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='json-schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='json-schema'), name='redoc'),
]


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", index),
    path("store/", include("store.urls")),
    path("auth/", include("djoser.urls")),
    path("auth/", include("djoser.urls.jwt")),
    path("__debug__/", include(debug_toolbar.urls)),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
]


urlpatterns += doc_patterns