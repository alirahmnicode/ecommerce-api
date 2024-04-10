from django.contrib import admin
from apps.carts import models


admin.site.register(models.Cart)
admin.site.register(models.CartItem)
