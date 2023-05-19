from django.shortcuts import render, get_object_or_404
from product.models import Product
from category.models import Category
from django.core.paginator import Paginator, EmptyPage, InvalidPage, PageNotAnInteger
from django.db.models import Q
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
    return render(request, "store/product-details.html", {"product": product})

def search(request):
    print("search")
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        print(f"keyword: {keyword}")
        if keyword:
            products = Product.objects.order_by('-created_date').filter(Q(description__icontains=keyword) | Q(name__icontains=keyword))
            products_count = products.count()
    context = {'products': products, 'products_count': products_count}
    return render(request, 'store/store.html', context)