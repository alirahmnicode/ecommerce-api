from rest_framework_nested import routers

from . import views


router = routers.DefaultRouter()
router.register("collections", views.CollectionViewSet)
router.register("customers", views.CustomerViewSet)
router.register("orders", views.OrderViewSet, basename="orders")




urlpatterns = router.urls + products_router.urls + carts_router.urls
