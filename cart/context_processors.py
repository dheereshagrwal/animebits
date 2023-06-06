from .models import Cart, CartItem
from utils.utils import calculate_totals


def get_cart_items(request):
    if request.user.is_superuser:
        return {}
    if request.user.is_authenticated:
        print(f"request.user {request.user}")
        cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        cart_items_count = cart_items.count()
    else:
        cart = Cart.objects.get(cart_id=request.session.get("cart_id"))
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        cart_items_count = cart_items.count()
    total, quantity, tax, grand_total, gift_charges = calculate_totals(cart_items)
    context = {
        "cart_items_count": cart_items_count,
        "cart_items": cart_items,
        "total": total,
        "quantity": quantity,
        "tax": tax,
        "grand_total": grand_total,
        "gift_charges": gift_charges,
    }
    return context
