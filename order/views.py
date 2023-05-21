from django.shortcuts import render, redirect
from cart.models import Cart, CartItem
from django.contrib.auth.decorators import login_required
from .forms import OrderForm
from .models import Order, OrderProduct, Payment
from product.models import Product
import uuid
import requests
from django.urls import reverse
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

@login_required(login_url="login")
def payment(request, order_id):
    # check if user is admin
    if request.user.is_superuser:
        return redirect("home")
    order = Order.objects.get(user=request.user, is_ordered=False, order_id=order_id)
    # check if order already exists
    url = f"https://sandbox.cashfree.com/pg/orders/{order_id}"

    headers = {
        "accept": "application/json",
        "x-client-id": "TEST389775d23cbf608bdfac150118577983",
        "x-client-secret": "TEST22f3e90a364cf1b20b9b5f7cdd0f7f82c8027e21",
        "x-api-version": "2022-09-01",
    }

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        payment_session_id = response.json()["payment_session_id"]
        print("payment_session_id", payment_session_id)
        context = {"payment_session_id": payment_session_id, "order": order}
        return render(request, "order/payment.html", context)

    url = "https://sandbox.cashfree.com/pg/orders"
    return_url = request.build_absolute_uri(reverse("payment_success"))[:-1]
    payload = {
        "customer_details": {
            "customer_id": "d6a-4ea6-9f19-07daecb93080",
            "customer_email": request.user.email,
            "customer_phone": "9411245528",
        },
        "order_meta": {"return_url": return_url + "?order_id={order_id}"},
        "order_id": order_id,
        "order_amount": order.grand_total,
        "order_currency": "INR",
    }
    headers = {
        "accept": "application/json",
        "x-client-id": "TEST389775d23cbf608bdfac150118577983",
        "x-client-secret": "TEST22f3e90a364cf1b20b9b5f7cdd0f7f82c8027e21",
        "x-api-version": "2022-09-01",
        "content-type": "application/json",
    }

    response = requests.post(url, json=payload, headers=headers)

    print(response.text)
    # get payment_session_id from the response
    payment_session_id = response.json()["payment_session_id"]
    print("payment_session_id", payment_session_id)
    context = {"payment_session_id": payment_session_id, "order": order}
    return render(request, "order/payment.html", context)


@login_required(login_url="login")
def payment_success(request):
    # get the order id from the url
    order_id = request.GET.get("order_id")
    # TODO: the below is the correct one
    # order = Order.objects.get(user=request.user, is_ordered=False, order_id=order_id)
    order = Order.objects.get(user=request.user, order_id=order_id)

    url = f"https://sandbox.cashfree.com/pg/orders/{order_id}/payments"
    headers = {
        "accept": "application/json",
        "x-client-id": "TEST389775d23cbf608bdfac150118577983",
        "x-client-secret": "TEST22f3e90a364cf1b20b9b5f7cdd0f7f82c8027e21",
        "x-api-version": "2022-09-01",
    }
    response = requests.get(url, headers=headers)
    response = response.json()[0]
    payment_id = response["cf_payment_id"]
    status = response["payment_status"]
    payment_method = response["payment_method"]
    payment_method = list(payment_method.keys())[0]
    print("payment_id", payment_id)
    print("status", status)
    print("payment_method", payment_method)
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
    cart = Cart.objects.get(user=request.user)
    cart_items = CartItem.objects.filter(cart=cart, is_active=True)
    for item in cart_items:
        order_product = OrderProduct()
        order_product.order = order
        order_product.payment = payment
        order_product.user = request.user
        order_product.product = item.product
        order_product.quantity = item.quantity
        order_product.product_price = item.product.price
        order_product.ordered = True
        order_product.save()

        cart_item = CartItem.objects.get(id=item.id)
        product_variation = cart_item.variations.all()
        order_product = OrderProduct.objects.get(id=order_product.id)
        order_product.variations.set(product_variation)
        order_product.save()
        # reduce the quantity of the sold products
        product = Product.objects.get(id=item.product.id)
        product.stock -= item.quantity
        product.save()
    
    # clear the cart
    cart.delete()
    ordered_products = OrderProduct.objects.filter(user=request.user, ordered=True)
    # send order received email to customer
    mail_subject = "Thank you for your order!"
    message = render_to_string(
        "order/order-received-email.html",
        {
            "user": request.user,
            "order": order,
        },
    )
    to_email = request.user.email
    send_email = EmailMessage(mail_subject, message, to=[to_email])
    print("send_email", send_email)
    send_email.send()
    context = {"order": order, "payment": payment, "ordered_products": ordered_products}
    return render(request, "order/payment-success.html", context)


@login_required(login_url="login")
def place_order(request):
    cart = Cart.objects.get(user=request.user)
    # check if there are any items in the cart
    cart_items = CartItem.objects.filter(cart=cart, is_active=True)
    cart_items_count = cart_items.count()
    if cart_items_count <= 0:
        return redirect("store")

    total, tax, grand_total, gift_charge = calculate_totals(cart_items)
    print(total, tax, grand_total, gift_charge)
    if request.method == "POST":
        form = OrderForm(request.POST)
        print(form.errors)
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
            data.gift_charge = gift_charge
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


def calculate_totals(cart_items):
    total = 0
    quantity = 0
    tax = 0
    grand_total = 0
    gift_charge = 0

    for cart_item in cart_items:
        for variation in cart_item.variations.all():
            if (
                variation.variation_category == "gift"
                and variation.variation_value == "gift"
            ):
                gift_charge += 10 * cart_item.quantity
        total += cart_item.product.price * cart_item.quantity
        quantity += cart_item.quantity

    tax = (5 * total) / 100
    grand_total = total + tax

    return total, tax, grand_total, gift_charge
