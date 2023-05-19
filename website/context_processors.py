from utils.utils import get_user_info
import uuid


def get_constant_data(request):
    cart_id = request.session.get("cart_id")
    if not cart_id:
        cart_id = str(uuid.uuid4()).replace("-", "")
        request.session["cart_id"] = cart_id
    
    user_info = get_user_info(request)
    return {"user_info": user_info}
