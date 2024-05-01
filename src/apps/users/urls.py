from rest_framework_nested import routers

from . import views


router = routers.DefaultRouter()
router.register("", views.CustomerViewSet)

customer_router = routers.NestedDefaultRouter(router, "", lookup="customer")
customer_router.register("address", views.CustomerAddressViewSet, basename="customer-address")

urlpatterns = router.urls + customer_router.urls
