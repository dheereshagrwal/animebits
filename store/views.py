from django.shortcuts import render, get_object_or_404, redirect
from product.models import Product, ProductGallery
from category.models import Category
from django.core.paginator import Paginator, EmptyPage, InvalidPage, PageNotAnInteger
from django.db.models import Q
from review.models import ReviewRating
from review.forms import ReviewForm
from order.models import OrderProduct
from utils.utils import get_user_info

# Create your views here.


def store(request, category_slug=None):
    categories = None
    products = Product.objects.filter(is_available=True).order_by("-created_date")
    if category_slug:
        categories = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=categories).order_by("-created_date")

    if request.GET.get("category"):
        # get all the categories from the request
        categories = request.GET.getlist("category")
        # get all the products that belong to the categories
        products = (
            products.filter(category__name__in=categories)
            .distinct()
            .order_by("-created_date")
        )

    if request.GET.get("sort"):
        sort = request.GET.get("sort")
        if sort == "best-sellers":
            products = products.order_by("-sold")
        elif sort == "price-low-to-high":
            products = products.order_by("price")
        elif sort == "price-high-to-low":
            products = products.order_by("-price")
        elif sort == "newest":
            products = products.order_by("-created_date")
        elif sort == "avg-rating":
            products = products.order_by("-avg_rating")
    
    products_count = products.count()
    paginator = Paginator(products, 12)
    page_number = request.GET.get("page")

    try:
        products = paginator.page(page_number)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    categories = Category.objects.all()
    context = {"products": products, "products_count": products_count, "categories": categories}
    return render(request, "store/store.html", context)


def product_details(request, category_slug, product_slug):
    try:
        product = get_object_or_404(
            Product, category__slug=category_slug, slug=product_slug
        )
    except Exception as e:
        raise e
    if request.user.is_authenticated:
        try:
            order_product = OrderProduct.objects.filter(
                user=request.user, product=product
            ).exists()
        except OrderProduct.DoesNotExist:
            order_product = None
    else:
        order_product = None
    # get the reviews
    reviews = ReviewRating.objects.filter(product=product, status=True)
    # get the product gallery
    product_gallery = ProductGallery.objects.filter(product=product)
    context = {
        "product": product,
        "order_product": order_product,
        "reviews": reviews,
        "product_gallery": product_gallery,
    }
    return render(request, "store/product-details.html", context)


def search(request):
    if "keyword" in request.GET:
        keyword = request.GET["keyword"]
        if keyword:
            products = Product.objects.order_by("-created_date").filter(
                Q(description__icontains=keyword) | Q(name__icontains=keyword)
            )
            products_count = products.count()
        else:
            return redirect("store")
    categories = Category.objects.all()
    context = {"products": products, "products_count": products_count, "categories": categories}
    return render(request, "store/store.html", context)


def submit_review(request, product_id):
    url = request.META.get("HTTP_REFERER")
    product = get_object_or_404(Product, id=product_id)
    user_info = get_user_info(request)
    if request.method == "POST":
        try:
            review = ReviewRating.objects.get(user=request.user, product=product)
            prev_rating = review.rating
            review.user_picture = user_info["picture"]
            form = ReviewForm(request.POST, instance=review)
            form.save()
            product.avg_rating = (product.avg_rating * product.total_reviews - prev_rating + form.cleaned_data["rating"]) / product.total_reviews
            product.save()

            return redirect(url)
        
        except ReviewRating.DoesNotExist:
            form = ReviewForm(request.POST)
            if form.is_valid():
                data = ReviewRating()
                data.title = form.cleaned_data["title"]
                data.rating = form.cleaned_data["rating"]
                data.review = form.cleaned_data["review"]
                data.ip = request.META.get("REMOTE_ADDR")
                data.user_picture = user_info["picture"]
                print("data.user_picture", data.user_picture)
                data.product = product
                data.user = request.user
                data.save()
                product.avg_rating = (product.avg_rating * product.total_reviews + data.rating) / (product.total_reviews + 1)
                product.total_reviews += 1
                product.save()

                print(f'product.avg_rating: {product.avg_rating} product.total_reviews: {product.total_reviews} data.rating: {data.rating}')
                
                return redirect(url)
