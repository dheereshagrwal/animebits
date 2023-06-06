from django.urls import path
from . import views

urlpatterns = [
    path("place-order/", views.place_order, name="place-order"),
    path("payment/<str:order_id>/", views.payment, name="payment"),
    path("payment-success/", views.payment_success, name="payment-success"),
]
