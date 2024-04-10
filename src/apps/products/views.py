from django.shortcuts import get_object_or_404
from django.db.models import Count
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework.viewsets import ModelViewSet
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from apps.products.models import Product, ProductImages, Collection, Review
from apps.products.filters import ProductFilter
from apps.products.permissions import IsAdminOrReadOnly
from apps.products.serializers import (
    ProductSerializer,
    ProductImageSerializer,
    CollectionSerializer,
    ReviewSerializer,
)

from apps.orders.models import OrderItem


class ProductViewSet(ModelViewSet):
    # create, retrieve, update, delete product
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ProductFilter
    pagination_class = PageNumberPagination
    permission_classes = [IsAdminOrReadOnly]
    search_fields = ["title", "description"]
    ordering_fields = ["unit_price", "last_update"]

    def get_serializer_context(self):
        return {"request": self.request}
    
    @method_decorator(cache_page(5 * 60))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        if OrderItem.objects.filter(product_id=kwargs["pk"]).count() > 0:
            return Response(
                {
                    "error": "Product cannot be deleted because its associated with an order item!"
                }
            )
        return super().destroy(request, *args, **kwargs)


class ProductImagesViewSet(ModelViewSet):
    queryset = ProductImages.objects.all()
    serializer_class = ProductImageSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        return ProductImages.objects.filter(product_id=self.kwargs["product_pk"])

    def get_serializer_context(self):
        return {"product_id": self.kwargs["product_pk"]}


class CollectionViewSet(ModelViewSet):
    # create, retrieve, update, delete collection
    queryset = Collection.objects.annotate(products_count=Count("products"))
    serializer_class = CollectionSerializer
    permission_classes = [IsAdminOrReadOnly]

    def destroy(self, request, pk, *args, **kwargs):
        collection = get_object_or_404(Collection, pk=pk)
        if collection.products.count() > 0:
            return Response(
                {
                    "error": "Collection cannot be deleted because its associated with a product item!"
                }
            )
        return super().destroy(request, *args, **kwargs)


class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        return Review.objects.filter(product_id=self.kwargs["product_pk"])

    def get_serializer_context(self):
        return {"product_id": self.kwargs["product_pk"]}
