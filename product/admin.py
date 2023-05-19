from django.contrib import admin
from .models import Product, Variation

# Register your models here.


class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "slug",
        "price",
        "stock",
        "category",
        "created_date",
        "modified_date",
        "is_available",
    )
    # description is prepopulated from name
    prepopulated_fields = {"slug": ("name",),}
    
class VariationAdmin(admin.ModelAdmin):
    list_display = ("product", "variation_category", "variation_value", "is_active")
    list_editable = ("is_active",)
    list_filter = ("product", "variation_category", "variation_value", "is_active")
    search_fields = ("product", "variation_category", "variation_value", "is_active")

admin.site.register(Product, ProductAdmin)
admin.site.register(Variation, VariationAdmin)