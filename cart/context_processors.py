from .models import Cart, CartItem


def get_cart_items(request):
    if request.user.is_superuser:
        return {}
    if request.user.is_authenticated:
        print(f'request.user {request.user}')
        cart = Cart.objects.get(user=request.user)
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        cart_items_count = cart_items.count()
    else:
        cart = Cart.objects.get(cart_id=request.session.get("cart_id"))
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        cart_items_count = cart_items.count()
        print(f'cart_id inside cart context processors {cart.cart_id}')
    return dict(cart_items_count=cart_items_count, cart_items=cart_items)
