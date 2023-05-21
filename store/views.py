from django.shortcuts import render, get_object_or_404, redirect
from product.models import Product
from category.models import Category
from django.core.paginator import Paginator, EmptyPage, InvalidPage, PageNotAnInteger
from django.db.models import Q
from review.models import ReviewRating
from review.forms import ReviewForm
from order.models import OrderProduct

# Create your views here.


def store(request, category_slug=None):
    categories = None
    products = Product.objects.filter(is_available=True).order_by("-created_date")

    if category_slug:
        categories = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=categories).order_by("-created_date")

    products_count = products.count()
    paginator = Paginator(products, 6)
    page_number = request.GET.get("page")

    try:
        products = paginator.page(page_number)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    context = {"products": products, "products_count": products_count}
    return render(request, "store/store.html", context)


def product_details(request, category_slug, product_slug):
    try:
        product = get_object_or_404(
            Product, category__slug=category_slug, slug=product_slug
        )
    except Exception as e:
        raise e
    try:
        order_product = OrderProduct.objects.filter(
            user=request.user, product=product
        ).exists()
    except OrderProduct.DoesNotExist:
        order_product = None

    # get the reviews
    reviews = ReviewRating.objects.filter(product=product, status=True)
    context = {"product": product, "order_product": order_product, "reviews": reviews}
    return render(request, "store/product-details.html", context)


def search(request):
    print("search")
    if "keyword" in request.GET:
        keyword = request.GET["keyword"]
        print(f"keyword: {keyword}")
        if keyword:
            products = Product.objects.order_by("-created_date").filter(
                Q(description__icontains=keyword) | Q(name__icontains=keyword)
            )
            products_count = products.count()
    context = {"products": products, "products_count": products_count}
    return render(request, "store/store.html", context)


def submit_review(request, product_id):
    url = request.META.get("HTTP_REFERER")
    if request.method == "POST":
        try:
            review = ReviewRating.objects.get(user=request.user, product__id=product_id)
            form = ReviewForm(request.POST, instance=review)
            form.save()
            return redirect(url)
        except ReviewRating.DoesNotExist:
            form = ReviewForm(request.POST)
            if form.is_valid():
                data = ReviewRating()
                data.title = form.cleaned_data["title"]
                data.rating = form.cleaned_data["rating"]
                data.review = form.cleaned_data["review"]
                data.ip = request.META.get("REMOTE_ADDR")
                data.product_id = product_id
                data.user = request.user
                data.save()
                return redirect(url)
