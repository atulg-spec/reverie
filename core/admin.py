from django.contrib import admin
from .models import SiteSettings


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ('store_name', 'phone', 'email')
    
    fieldsets = (
        ('General Information', {
            'fields': ('store_name', 'tagline', 'logo', 'banner_image')
        }),
        ('Contact & Address', {
            'fields': ('phone', 'email', 'address')
        }),
        ('Cashfree Payment Gateway', {
            'fields': ('cashfree_app_id', 'cashfree_secret_key', 'cashfree_is_sandbox'),
            'description': 'Enter your Cashfree API credentials here to enable automated payments.'
        }),
    )

    def has_add_permission(self, request):
        # Only allow one instance
        if SiteSettings.objects.exists():
            return False
        return True

    def has_delete_permission(self, request, obj=None):
        return False
