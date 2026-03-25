from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('', views.shop, name='shop'),
    path('p/<slug:slug>/', views.product_detail, name='product_detail'),
    path('<slug:category_slug>/', views.shop, name='shop_by_category'),
]
