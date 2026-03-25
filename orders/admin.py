from django.contrib import admin
from .models import Order, OrderItem, PaymentProof


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('product', 'product_name', 'size', 'quantity', 'price')


class PaymentProofInline(admin.StackedInline):
    model = PaymentProof
    extra = 0
    readonly_fields = ('screenshot', 'uploaded_at')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name', 'phone', 'total', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('full_name', 'email', 'phone')
    list_editable = ('status',)
    readonly_fields = ('full_name', 'email', 'phone', 'address', 'city', 'state', 'pincode', 'total', 'created_at')
    inlines = [OrderItemInline, PaymentProofInline]
    actions = ['mark_confirmed', 'mark_rejected']

    @admin.action(description='Mark selected orders as Confirmed')
    def mark_confirmed(self, request, queryset):
        queryset.update(status='confirmed')

    @admin.action(description='Mark selected orders as Rejected')
    def mark_rejected(self, request, queryset):
        queryset.update(status='rejected')
