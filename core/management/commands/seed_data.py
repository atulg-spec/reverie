from django.core.management.base import BaseCommand
from products.models import Category, Product, ProductImage
from core.models import SiteSettings


class Command(BaseCommand):
    help = 'Seed the database with neutral fashion items'

    def handle(self, *args, **options):
        self.stdout.write('Seeding database with neutral branding...')

        # Update or Create SiteSettings
        settings, _ = SiteSettings.objects.get_or_create(pk=1)
        settings.store_name = 'Elegance'
        settings.tagline = 'Premium Fashion Collection'
        settings.upi_id = 'elegance@upi'
        settings.phone = '+91 98765 43210'
        settings.email = 'hello@elegance.in'
        settings.address = 'Luxury Mall, Mumbai, Maharashtra 400001'
        settings.save()
        self.stdout.write(self.style.SUCCESS(f'SiteSettings Updated: {settings}'))

        # Create/Update Categories
        jutti_cat, _ = Category.objects.get_or_create(slug='rajasthani-ladies-jutti')
        jutti_cat.name = 'Premium Handcrafted Footwear'
        jutti_cat.description = 'Exquisite handcrafted traditional footwear with contemporary designs.'
        jutti_cat.save()

        frocks_cat, _ = Category.objects.get_or_create(slug='kids-fancy-frocks')
        frocks_cat.name = 'Kids Designer Collection'
        frocks_cat.description = 'Stylish and comfortable designer frocks for kids aged 0-5 years.'
        frocks_cat.save()
        
        self.stdout.write(self.style.SUCCESS('Categories Updated'))

        # Jutti Products (Now Handcrafted Footwear)
        jutti_products = [
            {
                'name': 'Royal Maroon Embroidered Footwear',
                'slug': 'royal-maroon-embroidered-jutti',
                'price': 1299,
                'original_price': 1799,
                'description': 'Exquisite footwear featuring intricate golden thread embroidery on a rich maroon base. Perfect for festive occasions and celebrations. Features a cushioned insole for all-day comfort.',
                'sizes': '5,6,7,8,9',
                'featured': True,
            },
            {
                'name': 'Golden Zari Design Mojari',
                'slug': 'golden-zari-work-mojari',
                'price': 1499,
                'original_price': 2199,
                'description': 'Stunning golden zari design footwear with intricate patterns. Handcrafted by master artisans using premium materials. Features a soft velvet lining.',
                'sizes': '5,6,7,8,9',
                'featured': True,
            },
        ]

        for data in jutti_products:
            product, created = Product.objects.get_or_create(slug=data['slug'], defaults={**data, 'category': jutti_cat})
            if not created:
                for key, value in data.items():
                    setattr(product, key, value)
                product.category = jutti_cat
                product.save()
            self.stdout.write(self.style.SUCCESS(f'  Updated: {product.name}'))

        # Frock Products (Now Kids Designer)
        frock_products = [
            {
                'name': 'Princess Pink Party Frock',
                'slug': 'princess-pink-layered-frock',
                'price': 899,
                'original_price': 1299,
                'description': 'Elegant pink layered frock with delicate lace trim. Features a comfortable cotton lining. Ideal for special occasions and birthday celebrations.',
                'sizes': '0-6M,6-12M,1-2Y,2-3Y,3-4Y,4-5Y',
                'featured': True,
            },
        ]

        for data in frock_products:
            product, created = Product.objects.get_or_create(slug=data['slug'], defaults={**data, 'category': frocks_cat})
            if not created:
                for key, value in data.items():
                    setattr(product, key, value)
                product.category = frocks_cat
                product.save()
            self.stdout.write(self.style.SUCCESS(f'  Updated: {product.name}'))

        self.stdout.write(self.style.SUCCESS('Database update complete!'))
