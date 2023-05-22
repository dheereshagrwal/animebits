from django.contrib import admin
from .models import Address
# Register your models here.
class AddressAdmin(admin.ModelAdmin):
    list_display = ("user", "phone", "address_1", "address_2", "state", "city", "zip", "created_at", "updated_at")
admin.site.register(Address, AddressAdmin)