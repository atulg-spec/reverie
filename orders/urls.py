from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('place-order/', views.place_order, name='place_order'),
    path('upload-payment/<int:order_id>/', views.upload_payment, name='upload_payment'),
    path('success/<int:order_id>/', views.order_success, name='order_success'),
    path('api/product/<int:product_id>/', views.get_product_data, name='product_data'),
]
