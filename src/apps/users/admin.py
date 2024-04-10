from django.contrib import admin
from django.urls import reverse
from django.db.models.aggregates import Count
from django.utils.html import format_html, urlencode
from django.contrib.contenttypes.admin import GenericTabularInline
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from apps.users.models import Customer
from apps.products.models import Product
# from apps.products.admin import ProductAdmin
# from tags.models import TaggedItem

from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "password1", "password2", "email"),
            },
        ),
    )


# class TagInline(GenericTabularInline):
#     autocomplete_fields = ["tag"]
#     model = TaggedItem


# class CustomProductAdmin(ProductAdmin):
#     inlines = [TagInline]


# admin.site.unregister(Product)
# admin.site.register(Product, CustomProductAdmin)

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ["first_name", "last_name", "membership", "orders"]
    list_editable = ["membership"]
    list_per_page = 10
    ordering = ["user__first_name", "user__last_name"]
    list_select_related = ["user"]
    search_fields = ["first_name__istartswith", "last_name__istartswith"]

    @admin.display(ordering="orders_count")
    def orders(self, customer):
        url = (
            reverse("admin:orders_order_changelist")
            + "?"
            + urlencode({"customer__id": str(customer.id)})
        )
        return format_html('<a href="{}">{} Orders</a>', url, customer.orders_count)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(orders_count=Count("order"))