from rest_framework_nested import routers

from . import views


router = routers.DefaultRouter()
router.register("products", views.ProductViewSet)
router.register("collections", views.CollectionViewSet)

products_router = routers.NestedDefaultRouter(router, "products", lookup="product")
products_router.register("reviews", views.ReviewViewSet, basename="products-reviews")
products_router.register(
    "images", views.ProductImagesViewSet, basename="products-images"
)

urlpatterns = router.urls + products_router.urls
