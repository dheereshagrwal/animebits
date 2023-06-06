from django.shortcuts import render, redirect, get_object_or_404
from product.models import Product, Variation
from utils.utils import calculate_totals
from .models import Cart, CartItem
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required

# Create your views here.


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
        is_cart_item_exists = CartItem.objects.filter(
            product=product, user=request.user, is_active=True
        ).exists()

        if is_cart_item_exists:
            cart_item = CartItem.objects.filter(
                product=product, user=request.user, is_active=True
            )

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
                item = CartItem.objects.create(
                    product=product, quantity=1, user=request.user
                )
                if product_variations:
                    item.variations.clear()
                    item.variations.add(*product_variations)
                item.save()
        else:
            cart_item = CartItem.objects.create(
                product=product, quantity=1, user=request.user
            )
            if product_variations:
                cart_item.variations.clear()
                cart_item.variations.add(*product_variations)
            cart_item.save()

        return redirect("cart")
    # not authenticated user
    else:
        cart_id = request.session.get("cart_id")
        cart = Cart.objects.get(cart_id=cart_id)

        is_cart_item_exists = CartItem.objects.filter(
            product=product, cart=cart, is_active=True
        ).exists()
        if is_cart_item_exists:
            cart_item = CartItem.objects.filter(
                product=product, cart=cart, is_active=True
            )
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
    product = get_object_or_404(Product, id=product_id)

    try:
        if request.user.is_authenticated:
            cart_item = CartItem.objects.get(
                product=product, user=request.user, id=cart_item_id
            )
        else:
            cart = Cart.objects.get(cart_id=request.session.get("cart_id"))
            cart_item = CartItem.objects.get(
                product=product, cart=cart, id=cart_item_id
            )

        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    except:
        pass
    return redirect("cart")


def remove_cart_item(request, product_id, cart_item_id):
    product = get_object_or_404(Product, id=product_id)
    if request.user.is_authenticated:
        cart_item = CartItem.objects.get(
            product=product, user=request.user, id=cart_item_id
        )
    else:
        cart = Cart.objects.get(cart_id=request.session.get("cart_id"))
        cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
    cart_item.delete()
    return redirect("cart")


def cart(request):
    return render(request, "store/cart.html")


@login_required(login_url="login")
def checkout(request):
    return render(request, "store/checkout.html")
