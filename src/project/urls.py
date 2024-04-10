from django.conf import settings
from django.conf.urls.static import static
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
    path("api/schema/yaml/", SpectacularAPIView.as_view(), name="schema"),
    path("api/schema/json/", SpectacularJSONAPIView.as_view(), name="json-schema"),
    path(
        "api/schema/swagger-ui/",
        SpectacularSwaggerView.as_view(url_name="json-schema"),
        name="swagger-ui",
    ),
    path(
        "api/schema/redoc/",
        SpectacularRedocView.as_view(url_name="json-schema"),
        name="redoc",
    ),
]

urlpatterns = [
    path("admin/", admin.site.urls),
    # local apps urls
    path("", index),
    path("store/products/", include("apps.products.urls")),
    path("store/carts/", include("apps.carts.urls")),
    path("store/orders/", include("apps.orders.urls")),
    path("store/customers/", include("apps.users.urls")),
    # third party urls
    path("auth/", include("djoser.urls")),
    path("auth/", include("djoser.urls.jwt")),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
]


urlpatterns += doc_patterns
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns.append(path("__debug__/", include(debug_toolbar.urls)))
