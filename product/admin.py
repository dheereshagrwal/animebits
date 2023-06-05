from django.contrib import admin
from .models import Product, Variation, ProductGallery
import admin_thumbnails

# Register your models here.


@admin_thumbnails.thumbnail("image")
class ProductGalleryInline(admin.TabularInline):
    model = ProductGallery
    extra = 1


@admin_thumbnails.thumbnail("image")
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
        "sold",
    )
    # description is prepopulated from name
    prepopulated_fields = {
        "slug": ("name",),
    }
    inlines = [ProductGalleryInline]
    search_fields = ["name", "slug", "description"]
    list_editable = ("price", "stock", "is_available", "sold")


class VariationAdmin(admin.ModelAdmin):
    list_display = ("product", "variation_category", "variation_value", "is_active")
    list_editable = ("is_active",)
    list_filter = ("product", "variation_category", "variation_value", "is_active")
    search_fields = ("product", "variation_category", "variation_value", "is_active")


admin.site.register(Product, ProductAdmin)
admin.site.register(Variation, VariationAdmin)
admin.site.register(ProductGallery)
