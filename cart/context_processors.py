from .models import Cart, CartItem


def get_cart_items_count(request):
    if "admin" in request.path:
        return {}
    elif not request.user.is_authenticated:
        return {}
    else:
        try:
            cart = Cart.objects.get(user=request.user)
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)
            cart_items_count = cart_items.count()
        except Cart.DoesNotExist:
            cart_items_count = 0
            cart_items = None
    return dict(cart_items_count=cart_items_count,cart_items=cart_items)
