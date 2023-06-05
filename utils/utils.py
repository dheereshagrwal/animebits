from allauth.socialaccount.models import SocialAccount

def get_user_info(request):
    user_info = {}
    if request.user.is_authenticated:
        try:
            extra_data = SocialAccount.objects.get(user=request.user).extra_data
            user_info["picture"] = extra_data["picture"]
            user_info["name"] = extra_data["name"]
        except:
            pass
    return user_info

def calculate_totals(cart_items):
    total = 0
    quantity = 0
    tax = 0
    grand_total = 0
    gift_charges = 0

    if cart_items:
        for cart_item in cart_items:
            for variation in cart_item.variations.all():
                if (
                    variation.variation_category == "gift"
                    and variation.variation_value == "gift"
                ):
                    gift_charges += 10 * cart_item.quantity
            total += cart_item.product.price * cart_item.quantity
            quantity += cart_item.quantity

        tax = (5 * total) / 100
        grand_total = total + tax

    return total, quantity, tax, grand_total, gift_charges