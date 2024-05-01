from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from apps.users.models import Address, Customer
from apps.users.permissions import IsAdminOrOwner
from apps.users.serializers import CustomerAddressSerializer, CustomerSerializer


class CustomerViewSet(ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsAdminUser]

    @action(detail=False, methods=["GET", "PUT"], permission_classes=[IsAuthenticated])
    def me(self, request):
        customer = Customer.objects.get(user_id=request.user.id)
        if request.method == "GET":
            serializer = CustomerSerializer(customer)
            return Response(serializer.data)
        else:
            serializer = CustomerSerializer(customer, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)

    def get_permissions(self):
        if self.request.method in "POST":
            self.permission_classes = [IsAuthenticated]

        return super().get_permissions()

    def get_serializer_context(self):
        return {"user_id": self.request.user.id}


class CustomerAddressViewSet(ModelViewSet):
    queryset = Address.objects.all()
    serializer_class = CustomerAddressSerializer

    def get_serializer_context(self):
        return {"customer_pk": self.kwargs["customer_pk"]}

    def get_permissions(self):
        if self.request.method in ["GET", "POST"]:
            self.permission_classes = [IsAuthenticated]
        else:
            self.permission_classes = [IsAdminOrOwner]

        return super().get_permissions()
