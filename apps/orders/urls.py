from rest_framework_nested import routers

from . import views


router = routers.DefaultRouter()
router.register("orders", views.OrderViewSet, basename="orders")

urlpatterns = router.urls
