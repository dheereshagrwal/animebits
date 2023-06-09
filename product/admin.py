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
        "category",
        'description',
        'avg_rating',
    )
    # description is prepopulated from name
    prepopulated_fields = {
        "slug": ("name",),
    }
    list_editable = ("price",)
    inlines = [ProductGalleryInline]
    search_fields = ["name", "slug", "description"]


class VariationAdmin(admin.ModelAdmin):
    list_display = ("product", "variation_category", "variation_value", "is_active")
    list_editable = ("is_active",)
    list_filter = ("product", "variation_category", "variation_value", "is_active")


admin.site.register(Product, ProductAdmin)
admin.site.register(Variation, VariationAdmin)
admin.site.register(ProductGallery)
