from django.contrib import admin
from .models import ReviewRating


class ReviewRatingAdmin(admin.ModelAdmin):
    list_display = ["user", "product", "title", "rating", "status", "created_at"]
    list_filter = ["status", "created_at", "user"]


# Register your models here.
admin.site.register(ReviewRating, ReviewRatingAdmin)