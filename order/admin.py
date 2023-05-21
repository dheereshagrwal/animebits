from django.contrib import admin
from .models import Order, Payment, OrderProduct
# Register your models here.
class OrderProductInline(admin.TabularInline):
    model = OrderProduct
    extra = 0
    readonly_fields = ["payment", "user", "product", "quantity", "product_price", "ordered"]
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        "user",
        "email",
        "order_id",
        "phone",
        "city",
        "status",
        "is_ordered",
        "created_at",
    ]
    list_filter = ["status", "is_ordered"]
    search_fields = ["order_id", "phone", "city"]
    list_per_page = 20
    inlines = [OrderProductInline]


admin.site.register(Order, OrderAdmin)
admin.site.register(Payment)
admin.site.register(OrderProduct)