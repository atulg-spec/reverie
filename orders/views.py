import json
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from products.models import Product
from core.models import SiteSettings
from .models import Order, OrderItem, PaymentProof
from .utils import create_cashfree_order, verify_cashfree_payment


def cart(request):
    return render(request, 'orders/cart.html')


def checkout(request):
    settings = SiteSettings.objects.first()
    return render(request, 'orders/checkout.html', {'settings': settings})


@require_POST
def place_order(request):
    try:
        data = json.loads(request.body)

        order = Order.objects.create(
            full_name=data['full_name'],
            email=data['email'],
            phone=data['phone'],
            address=data['address'],
            city=data['city'],
            state=data['state'],
            pincode=data['pincode'],
            total=data['total'],
            status='pending',
        )

        for item in data['items']:
            product = Product.objects.filter(id=item['product_id']).first()
            
            # Location-based safety check
            if product and product.is_meesho_product and data.get('state') == 'Uttar Pradesh':
                return JsonResponse({
                    'success': False, 
                    'error': f'"{product.name}" is only available via Meesho for delivery in Uttar Pradesh. Please remove it from your cart or change your delivery state.'
                }, status=400)

            OrderItem.objects.create(
                order=order,
                product=product,
                product_name=item['name'],
                size=item.get('size', ''),
                quantity=item['quantity'],
                price=item['price'],
            )

        # Create Cashfree Order if credentials exist
        payment_session_id = create_cashfree_order(order, request)

        return JsonResponse({
            'success': True, 
            'order_id': order.id,
            'payment_session_id': payment_session_id
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)


def verify_payment(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    cf_order_id = request.GET.get('order_id')
    
    if cf_order_id:
        is_success = verify_cashfree_payment(cf_order_id)
        if is_success:
            order.status = 'confirmed'
            order.notes += f"\nAutomated Payment Verified (CF Order ID: {cf_order_id})"
            order.save()
            return redirect('orders:order_success', order_id=order.id)
    
    # If verification fails or no cf_order_id, redirect to success but with pending status
    return redirect('orders:order_success', order_id=order.id)


@require_POST
def upload_payment(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    screenshot = request.FILES.get('screenshot')
    if screenshot:
        PaymentProof.objects.update_or_create(
            order=order,
            defaults={'screenshot': screenshot}
        )
        return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'error': 'No file uploaded'}, status=400)


def order_success(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    settings = SiteSettings.objects.first()
    return render(request, 'orders/order_success.html', {
        'order': order,
        'settings': settings,
    })


def get_product_data(request, product_id):
    """API endpoint for cart to fetch product details"""
    product = get_object_or_404(Product, id=product_id)
    image = product.primary_image
    return JsonResponse({
        'id': product.id,
        'name': product.name,
        'price': float(product.price),
        'image': image.image.url if image else '',
        'slug': product.slug,
    })
