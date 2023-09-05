from django.contrib import admin
from apps.vending.models import Product, VendingMachineSlot, User, Order


class UserAdmin(admin.ModelAdmin):
    list_display = ["username", "id", "credit"]


admin.site.register(User, UserAdmin)


class ProductAdmin(admin.ModelAdmin):
    list_display = ["name", "price", "created_at", "updated_at"]
    ordering = ["-created_at"]


admin.site.register(Product, ProductAdmin)


class SlotAdmin(admin.ModelAdmin):
    list_display = ["product", "quantity", "row", "column"]


admin.site.register(VendingMachineSlot, SlotAdmin)


class OrderAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "product", "slot", "created_at"]
    ordering = ["-created_at"]


admin.site.register(Order, OrderAdmin)
