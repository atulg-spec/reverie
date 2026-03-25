from django.db import models


class SiteSettings(models.Model):
    store_name = models.CharField(max_length=200, default='Elegance')
    tagline = models.CharField(max_length=500, default='Premium Fashion Collection')
    logo = models.ImageField(upload_to='site/', blank=True, null=True)
    banner_image = models.ImageField(upload_to='site/', blank=True, null=True, help_text='Main hero banner image')
    upi_id = models.CharField(max_length=200, blank=True, default='')
    qr_code = models.ImageField(upload_to='site/', blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, default='')
    email = models.EmailField(blank=True, default='')
    address = models.TextField(blank=True, default='')

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
