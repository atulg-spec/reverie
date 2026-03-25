from django.http import HttpResponse
from django.urls import reverse
from products.models import Product, Category
from django.utils import timezone

def sitemap(request):
    """
    Generate a dynamic sitemap.xml
    """
    base_url = f"{request.scheme}://{request.get_host()}"
    urls = []

    # Static Pages
    static_pages = [
        reverse('core:home'),
        reverse('products:shop'),
    ]
    for page in static_pages:
        urls.append({
            'loc': f"{base_url}{page}",
            'lastmod': timezone.now().strftime('%Y-%m-%d'),
            'changefreq': 'daily',
            'priority': '1.0' if page == '/' else '0.8'
        })

    # Categories
    for category in Category.objects.all():
        urls.append({
            'loc': f"{base_url}{reverse('products:shop')}?category={category.slug}",
            'lastmod': timezone.now().strftime('%Y-%m-%d'),
            'changefreq': 'weekly',
            'priority': '0.7'
        })

    # Products
    for product in Product.objects.filter(in_stock=True):
        urls.append({
            'loc': f"{base_url}{reverse('products:product_detail', args=[product.slug])}",
            'lastmod': product.updated_at.strftime('%Y-%m-%d') if hasattr(product, 'updated_at') else timezone.now().strftime('%Y-%m-%d'),
            'changefreq': 'weekly',
            'priority': '0.9'
        })

    xml_content = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml_content += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    for url in urls:
        xml_content += '  <url>\n'
        xml_content += f"    <loc>{url['loc']}</loc>\n"
        xml_content += f"    <lastmod>{url['lastmod']}</lastmod>\n"
        xml_content += f"    <changefreq>{url['changefreq']}</changefreq>\n"
        xml_content += f"    <priority>{url['priority']}</priority>\n"
        xml_content += '  </url>\n'
    xml_content += '</urlset>'

    return HttpResponse(xml_content, content_type='application/xml')

def robots_txt(request):
    """
    Generate robots.txt
    """
    base_url = f"{request.scheme}://{request.get_host()}"
    content = [
        "User-agent: *",
        "Allow: /",
        "Disallow: /admin/",
        "Disallow: /checkout/",
        "Disallow: /orders/success/",
        f"Sitemap: {base_url}/sitemap.xml"
    ]
    return HttpResponse("\n".join(content), content_type='text/plain')
