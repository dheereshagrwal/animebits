from django.shortcuts import render, redirect, get_object_or_404
from product.models import Product, Variation
from utils.utils import calculate_totals
from .models import Cart, CartItem
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required

# Create your views here.


# @login_required(login_url="login")
def add_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    product_variations = []
    if request.method == "POST":
        # check if "gift"is in request.POST
        if "gift" not in request.POST:
            request.POST._mutable = True
            request.POST["gift"] = "no"
        for item in request.POST:
            key = item
            value = request.POST[key]
            print(key, value)
            try:
                variation = Variation.objects.get(
                    product=product,
                    variation_category__iexact=key,
                    variation_value__iexact=value,
                )
                product_variations.append(variation)
            except:
                pass
    if request.user.is_authenticated:
        cart = Cart.objects.get(user=request.user)
    else:
        cart_id = request.session.get("cart_id")
        print("cart_id inside cart views", cart_id)
        cart = Cart.objects.get(cart_id=cart_id)

    is_cart_item_exists = CartItem.objects.filter(
        product=product, cart=cart, is_active=True
    ).exists()
    if is_cart_item_exists:
        cart_item = CartItem.objects.filter(product=product, cart=cart, is_active=True)
        # existing variations -> database
        # current variations -> product_variations
        # item_id -> database

        existing_variations_list = []
        id_list = []
        for item in cart_item:
            existing_variations = item.variations.all()
            existing_variations_list.append(list(existing_variations))
            id_list.append(item.id)

        if product_variations in existing_variations_list:
            index = existing_variations_list.index(product_variations)
            item = CartItem.objects.get(product=product, id=id_list[index])
            item.quantity += 1
            item.save()
        else:
            item = CartItem.objects.create(product=product, quantity=1, cart=cart)
            if product_variations:
                item.variations.clear()
                item.variations.add(*product_variations)
            item.save()
    else:
        cart_item = CartItem.objects.create(product=product, quantity=1, cart=cart)
        if product_variations:
            cart_item.variations.clear()
            cart_item.variations.add(*product_variations)
        cart_item.save()

    return redirect("cart")


def remove_cart(request, product_id, cart_item_id):
    if request.user.is_authenticated:
        cart = Cart.objects.get(user=request.user)
    else:
        cart = Cart.objects.get(cart_id=request.session.get("cart_id"))
    product = get_object_or_404(Product, id=product_id)
    try:
        cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    except:
        pass
    return redirect("cart")


def remove_cart_item(request, product_id, cart_item_id):
    if request.user.is_authenticated:
        cart = Cart.objects.get(user=request.user)
    else:
        cart = Cart.objects.get(cart_id=request.session.get("cart_id"))
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
    cart_item.delete()
    return redirect("cart")


def cart_checkout(request, template_name):
    total, quantity, tax, grand_total, gift_charges = 0, 0, 0, 0, 0
    context = {
        "total": total,
        "quantity": quantity,
        "tax": tax,
        "gift_charges": gift_charges,
        "grand_total": grand_total,
    }
    if request.user.is_superuser:
        return render(request, template_name, context)
    if request.user.is_authenticated:
        cart = Cart.objects.get(user=request.user)
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)
    else:
        cart = Cart.objects.get(cart_id=request.session.get("cart_id"))
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)

    total, quantity, tax, grand_total, gift_charges = calculate_totals(cart_items)

    return render(request, template_name, context)


# @login_required(login_url="login")
def cart(request):
    return cart_checkout(request, "store/cart.html")


@login_required(login_url="login")
def checkout(request):
    return cart_checkout(request, "store/checkout.html")
