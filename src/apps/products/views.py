from django.shortcuts import get_object_or_404
from django.db.models import Count
from rest_framework.viewsets import ModelViewSet
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend

from apps.products.models import Product, ProductImages, Collection, Review
from apps.products.filters import ProductFilter
from apps.products.permissions import IsAdminOrReadOnly
from apps.products.serializers import (
    ProductSerializer,
    ProductImageSerializer,
    ProductImageCreateSerializer,
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

    def get_serializer_class(self):
        if self.request.method == "POST":
            return ProductImageCreateSerializer

    def create(self, request, *args, **kwargs):
        images = request.data.pop("images")  

        if len(images) < 1:
            return Response("The images list is empty!")
        else:
            images_list = []

            for img in images:
                image = ProductImages.objects.create(product_id=kwargs["product_pk"], image=img)
                images_list.append(dict(id=image.id, url=image.get_image_url()))

            return Response(images_list, status=status.HTTP_201_CREATED)

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
