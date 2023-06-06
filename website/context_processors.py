from utils.utils import get_user_info
import uuid
from cart.models import Cart


def get_constant_data(request):
    # check if user is admin
    cart_id = request.session.get("cart_id")
    if not cart_id:
        cart_id = str(uuid.uuid4()).replace("-", "")
        request.session["cart_id"] = cart_id
    try:
        cart = Cart.objects.get(cart_id=cart_id)
    except Cart.DoesNotExist:
        cart = Cart.objects.create(cart_id=cart_id)

    print(
        f"cart.cart_id {cart.cart_id} cart.user {cart.user} request.user {request.user}"
    )
    user_info = get_user_info(request)
    return {"user_info": user_info, "cart": cart}
