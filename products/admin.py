from django.contrib import admin
from .models import Category, Product, ProductImage


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'is_meesho_product', 'featured', 'in_stock', 'created_at')
    list_filter = ('category', 'featured', 'in_stock', 'is_meesho_product')
    search_fields = ('name', 'description', 'meesho_url')
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ('featured', 'in_stock', 'price', 'is_meesho_product')
    inlines = [ProductImageInline]
    fieldsets = (
        (None, {
            'fields': ('name', 'slug', 'category', 'price', 'original_price', 'description', 'sizes')
        }),
        ('Status', {
            'fields': ('featured', 'in_stock')
        }),
        ('Meesho Integration', {
            'fields': ('is_meesho_product', 'meesho_url'),
            'description': 'If enabled, the product will redirect to Meesho instead of the local cart.'
        }),
    )
