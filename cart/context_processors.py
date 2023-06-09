from .models import Cart, CartItem
from utils.utils import calculate_totals


def get_cart_items_count(request):
    if request.user.is_superuser:
        cart = Cart.objects.get(cart_id=request.session.get("cart_id"))
        cart_items_count = CartItem.objects.filter(cart=cart).count()
    if request.user.is_authenticated:
        cart_items_count = CartItem.objects.filter(user=request.user).count()
    else:
        cart = Cart.objects.get(cart_id=request.session.get("cart_id"))
        cart_items_count = CartItem.objects.filter(cart=cart).count()
    context = {
        "cart_items_count": cart_items_count,
    }
    return context
