from django.shortcuts import render
from products.models import Product, Category
from .models import SiteSettings


def home(request):
    featured_products = Product.objects.filter(featured=True, in_stock=True)[:8]
    categories = Category.objects.all()
    settings = SiteSettings.objects.first()

    testimonials = [
        {
            'name': 'Priya Sharma',
            'location': 'Jaipur',
            'text': 'Absolutely love the jutti collection! The craftsmanship is exquisite and the colors are so vibrant. Received so many compliments!',
            'rating': 5,
        },
        {
            'name': 'Meera Patel',
            'location': 'Mumbai',
            'text': 'Ordered a frock for my daughter\'s birthday. The quality exceeded my expectations. She looked like a little princess!',
            'rating': 5,
        },
        {
            'name': 'Ananya Verma',
            'location': 'Delhi',
            'text': 'The Rajasthani juttis are simply gorgeous. Perfect blend of traditional art and modern comfort. Will order again!',
            'rating': 4,
        },
    ]

    context = {
        'featured_products': featured_products,
        'categories': categories,
        'settings': settings,
        'testimonials': testimonials,
    }
    return render(request, 'core/home.html', context)
