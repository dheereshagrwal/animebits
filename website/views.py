from django.shortcuts import render, redirect
from product.models import Product
from urllib.parse import urlparse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver
from order.models import Order
from cart.models import Cart, CartItem
from product.models import Product


@receiver(user_logged_in)
def post_login(sender, user, request, **kwargs):
    if request.user.is_superuser:
        return

    cart_id = request.session.get("cart_id")

    cart = Cart.objects.get(cart_id=cart_id)

    cart_items = CartItem.objects.filter(cart=cart)
    product_variations = []
    for cart_item in cart_items:
        variations = cart_item.variations.all()
        product_variations.append(list(variations))

    # get the cart items from the user who logged in
    user_cart_items = CartItem.objects.filter(user=user, is_active=True)
    existing_variations_list = []
    id_list = []
    for user_cart_item in user_cart_items:
        existing_variations = user_cart_item.variations.all()
        existing_variations_list.append(list(existing_variations))
        id_list.append(user_cart_item.id)

    for product_variation in product_variations:
        if product_variation in existing_variations_list:
            index = existing_variations_list.index(product_variation)
            item = CartItem.objects.get(id=id_list[index])
            item.quantity += 1
            item.user = user
            item.save()
        else:
            for cart_item in cart_items:
                cart_item.user = user
                cart_item.save()


# Create your views here.
def home(request):
    products = None
    products_count = 0
    # products = Product.objects.all().filter(is_available=True).order_by("-created_date")
    # products_count = products.count()
    context = {"products": products, "products_count": products_count}
    return render(request, "home.html", context)


def login(request):
    provider_login_url = "http://127.0.0.1:8000/accounts/google/login/"
    # Get the next url
    next_url = request.GET.get("next")
    if next_url:
        redirect_url = f"{provider_login_url}?next={next_url}"
    else:
        redirect_url = provider_login_url
    return redirect(redirect_url)


@login_required(login_url="login")
def my_orders(request):
    orders = Order.objects.order_by("-created_at").filter(
        user=request.user, is_ordered=True
    )
    context = {"orders": orders}
    if request.user.is_authenticated:
        return render(request, "my-orders.html", context)
    else:
        return redirect("login")