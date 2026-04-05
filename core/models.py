from django.db import models


class SiteSettings(models.Model):
    store_name = models.CharField(max_length=200, default='Elegance')
    tagline = models.CharField(max_length=500, default='Premium Fashion Collection')
    logo = models.ImageField(upload_to='site/', blank=True, null=True)
    banner_image = models.ImageField(upload_to='site/', blank=True, null=True, help_text='Main hero banner image')
    banner_image = models.ImageField(upload_to='site/', blank=True, null=True, help_text='Main hero banner image')
    phone = models.CharField(max_length=20, blank=True, default='')
    email = models.EmailField(blank=True, default='')
    address = models.TextField(blank=True, default='')

    # Cashfree Settings
    cashfree_app_id = models.CharField(max_length=200, blank=True, default='', help_text='Cashfree App ID')
    cashfree_secret_key = models.CharField(max_length=500, blank=True, default='', help_text='Cashfree Secret Key')
    cashfree_is_sandbox = models.BooleanField(default=True, help_text='Switch between Sandbox and Production modes')

    class Meta:
        verbose_name = 'Site Settings'
        verbose_name_plural = 'Site Settings'

    def __str__(self):
        return self.store_name

    def save(self, *args, **kwargs):
        # Ensure only one instance exists
        if not self.pk and SiteSettings.objects.exists():
            existing = SiteSettings.objects.first()
            self.pk = existing.pk
        super().save(*args, **kwargs)
