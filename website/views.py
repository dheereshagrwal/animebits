from django.shortcuts import render, redirect
from product.models import Product
from urllib.parse import urlparse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver
from order.models import Order
from cart.models import Cart, CartItem
from product.models import Product, Variation


@receiver(user_logged_in)
def post_login(sender, user, request, **kwargs):
    if request.user.is_superuser:
        return
    
    print("user_logged_in")
    cart_id = request.session.get("cart_id")
    print("cart_id post login", cart_id)

    is_cart_already_exists = Cart.objects.filter(user=user).exists()

    if not is_cart_already_exists:
        cart = Cart.objects.get(cart_id=cart_id)
        cart.user = user
        cart.save()


# Create your views here.
def home(request):
    products = Product.objects.all().filter(is_available=True).order_by("-created_date")
    products_count = products.count()
    context = {"products": products, "products_count": products_count}
    return render(request, "home.html", context)


def login(request):
    provider_login_url = "http://127.0.0.1:8000/accounts/google/login/"
    # Get the current relative URL
    current_url = request.META.get("HTTP_REFERER")
    current_url = urlparse(current_url).path
    redirect_url = f"{provider_login_url}?next={current_url}"
    print("redirect_url", redirect_url)
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
