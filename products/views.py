from django.shortcuts import render, get_object_or_404
from .models import Product, Category


def shop(request):
    products = Product.objects.filter(in_stock=True)
    categories = Category.objects.all()

    # Filter by category
    active_category = None
    category_slug = request.GET.get('category')
    if category_slug:
        active_category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=active_category)

    # Filter by price range
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)

    # Sorting
    sort = request.GET.get('sort', 'newest')
    if sort == 'price_low':
        products = products.order_by('price')
    elif sort == 'price_high':
        products = products.order_by('-price')
    elif sort == 'newest':
        products = products.order_by('-created_at')

    context = {
        'products': products,
        'categories': categories,
        'current_category': category_slug,
        'active_category': active_category,
        'current_sort': sort,
        'min_price': min_price or '',
        'max_price': max_price or '',
    }
    return render(request, 'products/shop.html', context)


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    related_products = Product.objects.filter(
        category=product.category, in_stock=True
    ).exclude(id=product.id)[:4]

    context = {
        'product': product,
        'related_products': related_products,
    }
    return render(request, 'products/product_detail.html', context)
