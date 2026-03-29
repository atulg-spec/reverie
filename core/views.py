from django.shortcuts import render
from products.models import Product, Category
from .models import SiteSettings


def home(request):
    featured_products = Product.objects.filter(featured=True, in_stock=True)[:8]
    categories = Category.objects.all()
    settings = SiteSettings.objects.first()

    testimonials = [
        {
            'name': 'Vikram Malhotra',
            'location': 'Mumbai',
            'text': "The tailoring on the 'Executive' series is impeccable. It's rare to find such quality at this price point. A staple for my boardroom meetings.",
            'rating': 5,
        },
        {
            'name': 'Siddharth Rao',
            'location': 'Bangalore',
            'text': "Officio has completely transformed my professional wardrobe. The slim-fit shirts are breathable and maintain their sharp look all day.",
            'rating': 5,
        },
        {
            'name': 'Arjun Mehta',
            'location': 'Delhi',
            'text': "Ordered the Combo pack and I'm impressed by the fabric quality. Fast delivery and premium packaging make it feel like a luxury purchase.",
            'rating': 5,
        },
    ]

    context = {
        'featured_products': featured_products,
        'categories': categories,
        'settings': settings,
        'testimonials': testimonials,
    }
    return render(request, 'core/home.html', context)
