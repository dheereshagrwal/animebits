from django.shortcuts import render, redirect
from cart.models import Cart, CartItem
from django.contrib.auth.decorators import login_required
from utils.utils import *
from .forms import OrderForm
from .models import Order, OrderProduct, Payment
from product.models import Product
import uuid
import requests
from django.urls import reverse
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.http import Http404

headers = {
    "accept": "application/json",
    "x-client-id": "TEST389775d23cbf608bdfac150118577983",
    "x-client-secret": "TEST22f3e90a364cf1b20b9b5f7cdd0f7f82c8027e21",
    "x-api-version": "2022-09-01",
}

@login_required(login_url="login")
def payment(request, order_id):
    # if request.user.is_superuser:
    #     return redirect("home")

    try:
        order = Order.objects.get(
            user=request.user, is_ordered=False, order_id=order_id
        )
    except Order.DoesNotExist:
        raise Http404("Order does not exist")

    payment_session_id = get_payment_session_id(order_id, order, request)
    print(
        "payment_session_id",
        payment_session_id,
        "order",
        order,
    )
    context = {"payment_session_id": payment_session_id, "order": order}
    return render(request, "order/payment.html", context)


def get_payment_session_id(order_id, order, request):
    url = f"https://sandbox.cashfree.com/pg/orders/{order_id}"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        payment_session_id = response.json()["payment_session_id"]
        return payment_session_id

    url = "https://sandbox.cashfree.com/pg/orders"
    return_url = request.build_absolute_uri(reverse("payment-success"))[:-1]
    payload = {
        "customer_details": {
            "customer_id": "d6a-4ea6-9f19-07daecb93080",
            "customer_email": request.user.email,
            "customer_phone": str(order.phone),
        },
        "order_meta": {"return_url": return_url + "?order_id={order_id}"},
        "order_id": order_id,
        "order_amount": order.grand_total,
        "order_currency": "INR",
    }
    headers["content-type"] = "application/json"

    response = requests.post(url, json=payload, headers=headers)
    payment_session_id = response.json()["payment_session_id"]
    return payment_session_id


@login_required(login_url="login")
def payment_success(request):
    # get the order id from the url
    order_id = request.GET.get("order_id")
    try:
        order = Order.objects.get(user=request.user, order_id=order_id)
    except Order.DoesNotExist:
        raise Http404("Order does not exist")
    # check if order is already ordered
    if order.is_ordered:
        ordered_products = OrderProduct.objects.filter(order=order)
        context = {"order": order, "ordered_products": ordered_products}
        return render(request, "order/payment-success.html", context)

    url = f"https://sandbox.cashfree.com/pg/orders/{order_id}/payments"
    response = requests.get(url, headers=headers)
    response = response.json()[0]
    payment_id = response["cf_payment_id"]
    status = response["payment_status"]
    if status != "SUCCESS":
        return redirect("payment", order_id=order_id)

    payment_method = response["payment_method"]
    payment_method = list(payment_method.keys())[0]
    payment = Payment(
        user=request.user,
        payment_id=payment_id,
        payment_method=payment_method,
        status=status,
        amount_paid=response["order_amount"],
    )
    payment.save()
    order.payment = payment
    order.is_ordered = True
    order.save()
    cart_items = CartItem.objects.filter(user=request.user, is_active=True)
    for cart_item in cart_items:
        order_product = OrderProduct()
        order_product.order = order
        order_product.payment = payment
        order_product.user = request.user
        order_product.product = cart_item.product
        order_product.quantity = cart_item.quantity
        order_product.ordered = True
        order_product.save()

        cart_item = CartItem.objects.get(id=cart_item.id)
        product_variation = cart_item.variations.all()
        order_product = OrderProduct.objects.get(id=order_product.id)
        order_product.variations.set(product_variation)
        order_product.save()
        # reduce the quantity of the sold products
        product = Product.objects.get(id=cart_item.product.id)
        product.stock -= cart_item.quantity
        product.sold += cart_item.quantity
        product.save()

    #
    ordered_products = OrderProduct.objects.filter(order=order)
    cart_items.delete()
    send_order_confirmation_email(request.user.email, order)
    context = {"order": order, "ordered_products": ordered_products}
    return render(request, "order/payment-success.html", context)

def send_order_confirmation_email(email, order):
    mail_subject = "Thank you for your order!"
    message = render_to_string("order/order-received-email.html", {"order": order})
    send_email = EmailMessage(mail_subject, message, to=[email])
    send_email.content_subtype = "html"
    send_email.send()

@login_required(login_url="login")
def place_order(request):
    # check if there are any items in the cart
    cart_items = CartItem.objects.filter(user=request.user, is_active=True)
    cart_items_count = cart_items.count()
    if cart_items_count <= 0:
        return redirect("store")

    total, quantity, tax, grand_total, gift_charges = calculate_totals(cart_items)
    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            order_id = "ORD-" + str(uuid.uuid4()).upper().replace("-", "")
            data = Order()
            data.user = request.user
            data.phone = form.cleaned_data["phone"]
            data.address_1 = form.cleaned_data["address_1"]
            data.address_2 = form.cleaned_data["address_2"]
            data.state = form.cleaned_data["state"]
            data.city = form.cleaned_data["city"]
            data.zip = form.cleaned_data["zip"]
            data.note = form.cleaned_data["note"]
            data.total = total
            data.tax = tax
            data.gift_charges = gift_charges
            data.grand_total = grand_total
            data.ip = request.META.get("REMOTE_ADDR")
            data.order_id = order_id
            data.save()
            order = Order.objects.get(
                user=request.user, is_ordered=False, order_id=order_id
            )
            context = {
                "order": order,
                "payment_session_id": None,
            }
            return render(request, "order/payment.html", context)
    else:
        return redirect("checkout")
