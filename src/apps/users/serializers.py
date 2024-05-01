from django.shortcuts import get_object_or_404
from rest_framework import serializers
from djoser.serializers import (
    UserSerializer as BaseUserSerializer,
    UserCreateSerializer as BaseUserCreateSerializer,
)

from rest_framework.exceptions import APIException
from apps.users.models import Address, Customer


class UserCreateSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        fields = ["id", "username", "password", "email", "first_name", "last_name"]


class UserCustomSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        fields = ["id", "username", "email", "first_name", "last_name"]


class CustomerAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ["id", "province", "city", "street", "number"]

    def create(self, validated_data):
        customer_pk = self.context["customer_pk"]
        customer = get_object_or_404(Customer, pk=customer_pk)
        return Address.objects.create(customer_id=customer.pk, **validated_data)


class CustomerSerializer(serializers.ModelSerializer):
    addresses = CustomerAddressSerializer(many=True, read_only=True)
    user = serializers.IntegerField(read_only=True)

    class Meta:
        model = Customer
        fields = ["id", "user", "phone", "membership", "addresses"]

    def create(self, validated_data):
        user_id = self.context["user_id"]
        customer = Customer.objects.filter(user_id=user_id).first()

        if customer is None:
            return Customer.objects.create(user_id=user_id, **validated_data)
        else:
            raise APIException("Customer is already exist!", code=400)
