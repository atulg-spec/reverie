import uuid
from cashfree_pg.models.create_order_request import CreateOrderRequest
from cashfree_pg.api_client import Cashfree
from core.models import SiteSettings

def get_cashfree_client():
    settings = SiteSettings.objects.first()
    if not settings or not settings.cashfree_app_id or not settings.cashfree_secret_key:
        return None
    
    return Cashfree(
        XClientId=settings.cashfree_app_id,
        XClientSecret=settings.cashfree_secret_key,
        XEnvironment=Cashfree.SANDBOX if settings.cashfree_is_sandbox else Cashfree.PRODUCTION
    )

def create_cashfree_order(order, request):
    client = get_cashfree_client()
    if not client:
        return None

    # Customer ID must be unique. Since we might not have a logged in user, 
    # we use a prefix + phone or a random UUID if phone is missing.
    customer_id = f"cust_{order.phone}" if order.phone else f"cust_{uuid.uuid4().hex[:10]}"
    
    # Return URL: Where Cashfree redirects after payment
    # We'll use our verify_payment view
    return_url = request.build_absolute_uri(f"/orders/verify-payment/{order.id}/")

    order_request = CreateOrderRequest(
        order_amount=float(order.total),
        order_currency="INR",
        order_id=f"ORDER_{order.id}_{uuid.uuid4().hex[:6]}", # Cashfree requires unique order_id even for retries
        customer_details={
            "customer_id": customer_id,
            "customer_email": order.email,
            "customer_phone": order.phone,
            "customer_name": order.full_name
        },
        order_meta={
            "return_url": return_url + "?order_id={order_id}"
        }
    )

    try:
        response = client.PGCreateOrder(x_api_version="2023-08-01", create_order_request=order_request)
        if hasattr(response, 'data'):
            return response.data.payment_session_id
    except Exception as e:
        print(f"Cashfree Error: {str(e)}")
        return None
    return None

def verify_cashfree_payment(cf_order_id):
    client = get_cashfree_client()
    if not client:
        return None

    try:
        response = client.PGOrderFetchPayments(x_api_version="2023-08-01", order_id=cf_order_id)
        if hasattr(response, 'data') and response.data:
            # Check if any payment is successful
            for payment in response.data:
                if payment.payment_status == "SUCCESS":
                    return True
    except Exception as e:
        print(f"Cashfree Verification Error: {str(e)}")
    
    return False
