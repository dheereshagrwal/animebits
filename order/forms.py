from django import forms
from .models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [
            "phone",
            "address_1",
            "address_2",
            "state",
            "city",
            "zip",
            "order_note",
        ]
